#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import venv
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable
from uuid import uuid4


LAMETRIC_THUMB_URL = "https://developer.lametric.com/content/apps/icon_thumbs/{id}"


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def require_leading_slash(path: str) -> str:
    if not path.startswith("/"):
        raise ValueError(f"Path must start with '/': {path}")
    return path


def _http_request(method: str, url: str, headers: dict[str, str] | None = None, body: bytes | None = None) -> bytes:
    req = urllib.request.Request(url, data=body, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        msg = payload.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"HTTP {exc.code} {method} {url}: {msg or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed {method} {url}: {exc}") from exc


def _http_get_json(url: str) -> object:
    raw = _http_request("GET", url, headers={"Accept": "application/json"})
    return json.loads(raw.decode("utf-8", errors="strict"))


def _parse_content_type(value: str | None) -> str:
    if not value:
        return ""
    return value.split(";", 1)[0].strip().lower()


@dataclass(frozen=True)
class MultipartFile:
    field_name: str
    filename: str
    content_type: str
    data: bytes


def _encode_multipart(fields: dict[str, str], files: Iterable[MultipartFile]) -> tuple[bytes, str]:
    boundary = f"----awtrixfs-{uuid4().hex}"
    chunks: list[bytes] = []

    def add(s: str) -> None:
        chunks.append(s.encode("utf-8"))

    for name, value in fields.items():
        add(f"--{boundary}\r\n")
        add(f'Content-Disposition: form-data; name="{name}"\r\n\r\n')
        add(f"{value}\r\n")

    for f in files:
        add(f"--{boundary}\r\n")
        add(
            f'Content-Disposition: form-data; name="{f.field_name}"; filename="{f.filename}"\r\n'
            f"Content-Type: {f.content_type}\r\n\r\n"
        )
        chunks.append(f.data)
        add("\r\n")

    add(f"--{boundary}--\r\n")
    return b"".join(chunks), boundary


def _content_type_for_path(path: str) -> str:
    lower = path.lower()
    if lower.endswith(".gif"):
        return "image/gif"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    return "application/octet-stream"


def _ensure_pillow() -> None:
    try:
        import PIL  # noqa: F401

        return
    except Exception:
        pass

    venv_dir = os.environ.get(
        "AWTRIX_FS_VENV_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), ".venv"),
    )
    venv_python = os.path.join(venv_dir, "bin", "python")
    venv_pip = os.path.join(venv_dir, "bin", "pip")

    if not os.path.exists(venv_python):
        eprint(f"Creating venv at {venv_dir} for Pillow...")
        venv.EnvBuilder(with_pip=True, clear=False).create(venv_dir)

    eprint("Pillow is required for PNG/JPEG -> JPG conversion; installing into venv...")
    try:
        subprocess.check_call([venv_pip, "install", "Pillow"])
    except Exception as exc:
        raise RuntimeError(
            f"Failed to install Pillow into venv at {venv_dir}. "
            f"Try: {venv_pip} install Pillow"
        ) from exc

    try:
        site_dir = (
            subprocess.check_output(
                [venv_python, "-c", "import site; print(site.getsitepackages()[0])"],
                text=True,
            )
            .strip()
        )
        if site_dir and site_dir not in sys.path:
            sys.path.insert(0, site_dir)
    except Exception as exc:
        raise RuntimeError(f"Installed Pillow but failed to locate site-packages in {venv_dir}") from exc


def _convert_to_jpeg(image_bytes: bytes) -> bytes:
    _ensure_pillow()
    from PIL import Image  # type: ignore

    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        if img.mode in ("RGBA", "LA") or ("transparency" in getattr(img, "info", {})):
            rgba = img.convert("RGBA")
            bg = Image.new("RGBA", rgba.size, (0, 0, 0, 255))
            bg.alpha_composite(rgba)
            rgb = bg.convert("RGB")
        else:
            rgb = img.convert("RGB")

        out = BytesIO()
        rgb.save(out, format="JPEG", quality=95, optimize=True)
        return out.getvalue()


class AwtrixClient:
    def __init__(self, host: str) -> None:
        self.base_url = host

    @property
    def _origin(self) -> str:
        if self.base_url.startswith("http://") or self.base_url.startswith("https://"):
            return self.base_url.rstrip("/")
        return f"http://{self.base_url}".rstrip("/")

    def status(self) -> dict[str, object]:
        return _http_get_json(f"{self._origin}/status")  # type: ignore[return-value]

    def list_dir(self, dir_path: str) -> list[dict[str, str]]:
        require_leading_slash(dir_path)
        url = f"{self._origin}/list?{urllib.parse.urlencode({'dir': dir_path})}"
        return _http_get_json(url)  # type: ignore[return-value]

    def upload_bytes(self, dest_path: str, data: bytes, content_type: str | None = None) -> None:
        dest_path = require_leading_slash(dest_path)
        body, boundary = _encode_multipart(
            fields={},
            files=[
                MultipartFile(
                    field_name="data",
                    filename=dest_path,
                    content_type=content_type or _content_type_for_path(dest_path),
                    data=data,
                )
            ],
        )
        _http_request(
            "POST",
            f"{self._origin}/edit",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            body=body,
        )

    def create_path(self, path: str) -> None:
        path = require_leading_slash(path)
        body, boundary = _encode_multipart(fields={"path": path}, files=[])
        _http_request(
            "PUT",
            f"{self._origin}/edit",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            body=body,
        )

    def rename(self, old_path: str, new_path: str) -> None:
        old_path = require_leading_slash(old_path)
        new_path = require_leading_slash(new_path)
        body, boundary = _encode_multipart(fields={"path": old_path, "src": new_path}, files=[])
        _http_request(
            "PUT",
            f"{self._origin}/edit",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            body=body,
        )

    def delete(self, path: str) -> None:
        path = require_leading_slash(path)
        body, boundary = _encode_multipart(fields={"path": path}, files=[])
        _http_request(
            "DELETE",
            f"{self._origin}/edit",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            body=body,
        )


def cmd_status(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    st = client.status()
    print(json.dumps(st, indent=2, sort_keys=True))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    entries = client.list_dir(args.dir)
    if args.json:
        print(json.dumps(entries, indent=2, sort_keys=True))
        return 0
    for entry in entries:
        kind = entry.get("type", "?")
        name = entry.get("name", "?")
        size = entry.get("size", "")
        print(f"{kind:4} {size:>8} {name}")
    return 0


def _bytes_int(value: object) -> int:
    try:
        return int(str(value))
    except Exception:
        return 0


def _print_space_delta(before: dict[str, object], after: dict[str, object]) -> None:
    total = _bytes_int(after.get("totalBytes"))
    used_before = _bytes_int(before.get("usedBytes"))
    used_after = _bytes_int(after.get("usedBytes"))
    free_after = max(0, total - used_after)
    print(f"flash: used {used_before} -> {used_after} bytes; free now {free_after} bytes (total {total})")


def cmd_upload(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    dest = require_leading_slash(args.dest)
    with open(args.local, "rb") as f:
        payload = f.read()

    before = client.status()
    free = _bytes_int(before.get("totalBytes")) - _bytes_int(before.get("usedBytes"))
    if not args.force and free > 0 and len(payload) > free:
        raise RuntimeError(f"Not enough free space: need {len(payload)} bytes, have {free} bytes (use --force to try anyway)")

    client.upload_bytes(dest, payload)
    after = client.status()
    _print_space_delta(before, after)
    print(f"uploaded {args.local} -> {dest} ({len(payload)} bytes)")
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    client.create_path(args.path)
    print(f"created {args.path}")
    return 0


def cmd_rename(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    client.rename(args.old, args.new)
    print(f"renamed {args.old} -> {args.new}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    client = AwtrixClient(args.host)
    client.delete(args.path)
    print(f"deleted {args.path}")
    return 0


def cmd_icons_list(args: argparse.Namespace) -> int:
    args.dir = "/ICONS"
    return cmd_list(args)


def cmd_icons_import_lametric(args: argparse.Namespace) -> int:
    icon_id = str(args.id).strip()
    if not icon_id.isdigit():
        raise ValueError("Icon ID must be numeric")

    url = LAMETRIC_THUMB_URL.format(id=icon_id)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        content_type = _parse_content_type(resp.headers.get("content-type"))
        raw = resp.read()

    if content_type == "image/gif":
        payload = raw
        ext = ".gif"
        out_type = "image/gif"
    elif content_type in ("image/png", "image/jpeg", "image/jpg"):
        payload = _convert_to_jpeg(raw)
        ext = ".jpg"
        out_type = "image/jpeg"
    else:
        raise RuntimeError(f"Unsupported LaMetric content-type: {content_type or 'unknown'}")

    dest = require_leading_slash(os.path.join(args.dest_dir, f"{icon_id}{ext}").replace("\\", "/"))
    client = AwtrixClient(args.host)

    before = client.status()
    free = _bytes_int(before.get("totalBytes")) - _bytes_int(before.get("usedBytes"))
    if not args.force and free > 0 and len(payload) > free:
        raise RuntimeError(f"Not enough free space: need {len(payload)} bytes, have {free} bytes (use --force to try anyway)")

    client.upload_bytes(dest, payload, content_type=out_type)
    after = client.status()
    _print_space_delta(before, after)
    print(f"imported LaMetric {icon_id} ({content_type}) -> {dest} ({len(payload)} bytes)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AWTRIX HTTP filesystem helper")
    p.add_argument("--host", required=True, help="AWTRIX host or base URL (e.g., 10.10.20.112 or http://10.10.20.112)")

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Print /status JSON")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("list", help="List directory via /list?dir=...")
    s.add_argument("--json", action="store_true", help="Output raw JSON")
    s.add_argument("dir", help="Directory path on device (must start with /)")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("upload", help="Upload local file to device (POST /edit)")
    s.add_argument("--force", action="store_true", help="Skip free-space check")
    s.add_argument("local", help="Local file path")
    s.add_argument("dest", help="Destination path on device (must start with /)")
    s.set_defaults(func=cmd_upload)

    s = sub.add_parser("create", help="Create empty file/path (PUT /edit with path=...)")
    s.add_argument("path", help="Path to create (must start with /)")
    s.set_defaults(func=cmd_create)

    s = sub.add_parser("rename", help="Rename/move a file (PUT /edit with path+src)")
    s.add_argument("old", help="Existing path (must start with /)")
    s.add_argument("new", help="New path (must start with /)")
    s.set_defaults(func=cmd_rename)

    s = sub.add_parser("delete", help="Delete a file (DELETE /edit with path=...)")
    s.add_argument("path", help="Path to delete (must start with /)")
    s.set_defaults(func=cmd_delete)

    icons = sub.add_parser("icons", help="Icon-specific helpers")
    icons_sub = icons.add_subparsers(dest="icons_cmd", required=True)

    s = icons_sub.add_parser("list", help="List /ICONS")
    s.add_argument("--json", action="store_true", help="Output raw JSON")
    s.set_defaults(func=cmd_icons_list)

    s = icons_sub.add_parser("import-lametric", help="Download LaMetric icon and save to /ICONS/<id>.jpg (GIF preserved)")
    s.add_argument("--dest-dir", default="/ICONS", help="Destination directory on device (default: /ICONS)")
    s.add_argument("--force", action="store_true", help="Skip free-space check")
    s.add_argument("id", help="LaMetric icon ID (numeric)")
    s.set_defaults(func=cmd_icons_import_lametric)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        eprint("Interrupted")
        return 130
    except Exception as exc:
        eprint(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
