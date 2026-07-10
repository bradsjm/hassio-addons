#!/usr/bin/env python3
"""Offline behavior checks for the Hyperion.NG 2.2.1 builder migration.

Run directly with ``python3 addon-hyperion-ng/tests/test_migration.py``.  The
tests replace curl at the process boundary, so they require neither Docker nor
network access.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ADDON_DIR = REPO_ROOT / "addon-hyperion-ng"
DOWNLOADER = ADDON_DIR / "download-hyperion.sh"
UPDATE_VERSION = REPO_ROOT / ".github/scripts/update-hyperion-version.sh"

DOWNLOAD_CURL = r'''#!/usr/bin/env python3
import io
import os
from pathlib import Path
import sys
import tarfile

arguments = sys.argv[1:]
url = arguments[-1]
with Path(os.environ["CURL_LOG"]).open("a") as log:
    log.write(url + "\n")

output = Path(arguments[arguments.index("--output") + 1])
with tarfile.open(output, "w:gz", compresslevel=0) as archive:
    entry = tarfile.TarInfo("bin/hyperiond")
    entry.mode = 0o755
    entry.size = 10 * 1024 * 1024
    archive.addfile(entry, io.BytesIO(b"\0" * entry.size))
'''

UPDATE_CURL = r'''#!/usr/bin/env python3
import os
from pathlib import Path
import sys

url = sys.argv[-1]
with Path(os.environ["CURL_LOG"]).open("a") as log:
    log.write(url + "\n")

if url.endswith("/releases/latest"):
    print('{"tag_name":"2.2.2"}')
    raise SystemExit(0)
if url.endswith("Hyperion-2.2.2-Linux-amd64.tar.gz"):
    raise SystemExit(0)
if url.endswith("Hyperion-2.2.2-Linux-arm64.tar.gz"):
    print("asset intentionally absent", file=sys.stderr)
    raise SystemExit(22)
raise SystemExit("unexpected curl URL: " + url)
'''


class HyperionMigrationTests(unittest.TestCase):
    """Public downloader, update-helper, and add-on metadata contracts."""

    def _make_executable(self, directory: Path, name: str, contents: str) -> Path:
        executable = directory / name
        executable.write_text(contents)
        executable.chmod(0o755)
        return executable

    def test_downloader_maps_supported_architectures_to_221_assets(self) -> None:
        """The supported HA architectures select Hyperion's 2.2.1 asset names."""
        expected_urls = {
            "amd64": "https://github.com/hyperion-project/hyperion.ng/releases/download/2.2.1/Hyperion-2.2.1-Linux-amd64.tar.gz",
            "aarch64": "https://github.com/hyperion-project/hyperion.ng/releases/download/2.2.1/Hyperion-2.2.1-Linux-arm64.tar.gz",
        }

        for architecture, expected_url in expected_urls.items():
            with self.subTest(architecture=architecture), tempfile.TemporaryDirectory() as tempdir:
                root = Path(tempdir)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                self._make_executable(bin_dir, "curl", DOWNLOAD_CURL)
                curl_log = root / "curl.log"
                output_dir = root / "output"
                output_dir.mkdir()

                result = subprocess.run(
                    ["bash", str(DOWNLOADER), "2.2.1", architecture, str(output_dir)],
                    env=os.environ | {"PATH": f"{bin_dir}:{os.environ['PATH']}", "CURL_LOG": str(curl_log)},
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(curl_log.read_text().splitlines(), [expected_url])

    def test_downloader_rejects_armhf_before_requesting_an_asset(self) -> None:
        """The removed armhf platform cannot trigger a download."""
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            self._make_executable(bin_dir, "curl", DOWNLOAD_CURL)
            curl_log = root / "curl.log"
            output_dir = root / "output"
            output_dir.mkdir()

            result = subprocess.run(
                ["bash", str(DOWNLOADER), "2.2.1", "armhf", str(output_dir)],
                env=os.environ | {"PATH": f"{bin_dir}:{os.environ['PATH']}", "CURL_LOG": str(curl_log)},
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsupported architecture: armhf", result.stderr)
            self.assertFalse(curl_log.exists())

    def test_update_helper_does_not_mutate_config_when_a_required_asset_is_missing(self) -> None:
        """A failed arm64 validation stops the version update before its write."""
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = Path(tempdir)
            config_dir = workspace / "addon-hyperion-ng"
            config_dir.mkdir()
            config_file = config_dir / "config.json"
            config = json.loads((ADDON_DIR / "config.json").read_text())
            config["version"] = "2.0.16"
            config_file.write_text(json.dumps(config, indent=2) + "\n")
            before = config_file.read_text()

            bin_dir = workspace / "bin"
            bin_dir.mkdir()
            self._make_executable(bin_dir, "curl", UPDATE_CURL)
            curl_log = workspace / "curl.log"
            github_env = workspace / "github.env"

            result = subprocess.run(
                ["bash", str(UPDATE_VERSION)],
                env=os.environ
                | {
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "CURL_LOG": str(curl_log),
                    "GITHUB_ENV": str(github_env),
                    "GITHUB_WORKSPACE": str(workspace),
                },
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Required asset not found for arm64", result.stderr)
            self.assertEqual(config_file.read_text(), before)
            self.assertEqual(
                curl_log.read_text().splitlines(),
                [
                    "https://api.github.com/repos/hyperion-project/hyperion.ng/releases/latest",
                    "https://github.com/hyperion-project/hyperion.ng/releases/download/2.2.2/Hyperion-2.2.2-Linux-amd64.tar.gz",
                    "https://github.com/hyperion-project/hyperion.ng/releases/download/2.2.2/Hyperion-2.2.2-Linux-arm64.tar.gz",
                ],
            )

    def test_config_exposes_the_fixed_221_host_network_contract(self) -> None:
        """Metadata advertises only supported platforms and Hyperion's fixed UI."""
        config = json.loads((ADDON_DIR / "config.json").read_text())

        self.assertEqual(config["version"], "2.2.1")
        self.assertEqual(config["arch"], ["amd64", "aarch64"])
        self.assertIs(config["host_network"], True)
        self.assertEqual(config["image"], "docker.io/bradsjm/addon-hyperion-ng")
        self.assertEqual(config["webui"], "http://[HOST]:[PORT:8090]")
        self.assertNotIn("ports", config)
        self.assertNotIn("ports_description", config)

    def test_legacy_builder_metadata_files_are_removed(self) -> None:
        """The migration leaves no obsolete builder or per-architecture metadata."""
        for legacy_path in (
            REPO_ROOT / ".github/scripts/build-hyperion.sh",
            REPO_ROOT / ".github/scripts/download-hyperion.sh",
            ADDON_DIR / "build.json",
        ):
            with self.subTest(path=legacy_path):
                self.assertFalse(legacy_path.exists())


if __name__ == "__main__":
    unittest.main()
