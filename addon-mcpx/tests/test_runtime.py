#!/usr/bin/env python3
"""Behavior checks for the MCPX add-on startup contract.

Run directly with ``python3 addon-mcpx/tests/test_runtime.py``.  It uses only
the standard library and replaces HA/container executables at the process
boundary; no Home Assistant installation, Docker daemon, or root paths are
needed.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ADDON_DIR = REPO_ROOT / "addon-mcpx"
RUN_SOURCE = ADDON_DIR / "rootfs/etc/services.d/mcpx/run"

MOCK = r'''#!/usr/bin/env python3
import os
from pathlib import Path
import sys

name = Path(sys.argv[0]).name
args = sys.argv[1:]
log = Path(os.environ["TEST_LOG"])

def record(value):
    with log.open("a") as handle:
        handle.write(value + "\n")

if name == "bashio::config.has_value":
    option = {"allowed_ip_ranges": "TEST_ALLOWED_IP_RANGES", "cors_origins": "TEST_CORS_ORIGINS"}[args[0]]
    sys.exit(0 if os.environ.get(option, "") else 1)
elif name == "bashio::config":
    option = {
        "log_level": "TEST_LOG_LEVEL",
        "access_log_level": "TEST_ACCESS_LOG_LEVEL",
        "auth_key": "TEST_AUTH_KEY",
        "enable_metrics": "TEST_ENABLE_METRICS",
        "enable_docker_mcp": "TEST_ENABLE_DOCKER_MCP",
        "allowed_ip_ranges": "TEST_ALLOWED_IP_RANGES",
        "cors_origins": "TEST_CORS_ORIGINS",
    }[args[0]]
    defaults = {"log_level": "info", "access_log_level": "debug", "enable_metrics": "false", "enable_docker_mcp": "false"}
    print(os.environ.get(option, defaults.get(args[0], "")))
elif name.startswith("bashio::log."):
    record(f"{name.removeprefix('bashio::log.')}:" + " ".join(args))
elif name == "chown":
    for path in args[1:]:
        record(f"chown:{args[0]}:{path}")
elif name == "stat":
    print("0")
elif name == "addgroup":
    record("addgroup:" + " ".join(args))
elif name == "hexdump":
    print("123456789abc", end="")
elif name == "su-exec":
    user, command, *command_args = args
    if command == "docker":
        record(f"docker:{user}")
        sys.exit(0 if os.environ.get("TEST_DOCKER_ACCESS", "ok") == "ok" else 1)
    if command == "/usr/local/bin/generate-config.sh":
        record(f"generate:{user}")
    elif command == "serve":
        record(f"serve:{user}")
    elif command == "node":
        record(f"node:{user}:{Path.cwd()}")
        with Path(os.environ["TEST_ENV_FILE"]).open("w") as handle:
            for key in ("APP_CONFIG_PATH", "SERVERS_CONFIG_PATH", "AUDIT_LOG_DIR", "DIND_ENABLED", "AUTH_KEY", "ALLOWED_IP_RANGES", "CORS_ORIGINS"):
                handle.write(f"{key}={os.environ.get(key, '')}\n")
    else:
        record(f"unexpected:{command}")
        sys.exit(1)
else:
    raise SystemExit(f"unexpected mock executable {name}")
'''


class McpxRuntimeTests(unittest.TestCase):
    """Observable startup behavior for config and optional Docker support."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.socket: socket.socket | None = None
        self._make_mocks()

    def tearDown(self) -> None:
        if self.socket is not None:
            self.socket.close()
        self.tempdir.cleanup()

    def _make_mocks(self) -> None:
        mock = self.root / "mock.py"
        mock.write_text(MOCK)
        mock.chmod(0o755)
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        for command in ("bashio::config", "bashio::config.has_value", "bashio::log.error", "bashio::log.info", "chown", "stat", "addgroup", "hexdump", "su-exec"):
            (bin_dir / command).symlink_to(mock)

    def _start_socket(self) -> None:
        docker_socket = self.root / "docker.sock"
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.bind(str(docker_socket))
        self.socket.listen()

    def _run(self, **options: str) -> subprocess.CompletedProcess[str]:
        run_copy = self.root / "run"
        source = RUN_SOURCE.read_text()
        source = source.replace("config_dir=/config", 'config_dir="${TEST_CONFIG_DIR:?}"')
        source = source.replace("data_dir=/data", 'data_dir="${TEST_DATA_DIR:?}"')
        source = source.replace("docker_socket=/var/run/docker.sock", 'docker_socket="${TEST_DOCKER_SOCKET:?}"')
        source = source.replace("< /tmp/version.env", '< "${TEST_VERSION_FILE:?}"')
        run_copy.write_text(source)

        (self.root / "version.env").write_text("0.2.0-upstream\n")
        environment = os.environ | {
            "PATH": f"{self.root / 'bin'}:{os.environ['PATH']}",
            "TEST_LOG": str(self.root / "log"),
            "TEST_ENV_FILE": str(self.root / "environment"),
            "TEST_CONFIG_DIR": str(self.root / "config"),
            "TEST_DATA_DIR": str(self.root / "data"),
            "TEST_DOCKER_SOCKET": str(self.root / "docker.sock"),
            "TEST_VERSION_FILE": str(self.root / "version.env"),
            **options,
        }
        return subprocess.run(["bash", str(run_copy)], env=environment, text=True, capture_output=True, check=False)

    def _log(self) -> list[str]:
        log = self.root / "log"
        return log.read_text().splitlines() if log.exists() else []

    def _environment(self) -> dict[str, str]:
        return dict(line.split("=", 1) for line in (self.root / "environment").read_text().splitlines())

    def test_uses_addon_config_and_preserves_existing_server_definitions(self) -> None:
        config = self.root / "config"
        data = self.root / "data"
        config.mkdir()
        data.mkdir()
        (config / "app.yaml").write_text(
            "customSetting: retained\nauth:\n  enabled: false\n  header: custom-header\notherSetting: retained\n"
        )
        servers = '{"mcpServers":{"preserved":{"command":"example"}}}\n'
        (config / "mcp.json").write_text(servers)

        result = self._run(
            TEST_AUTH_KEY="secret",
            TEST_ALLOWED_IP_RANGES="10.0.0.0/8\n192.168.1.0/24",
            TEST_CORS_ORIGINS="https://one.example\nhttps://two.example",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((config / "mcp.json").read_text(), servers)
        self.assertIn("customSetting: retained", (config / "app.yaml").read_text())
        self.assertIn("  enabled: true", (config / "app.yaml").read_text())
        self.assertIn("  header: x-lunar-api-key", (config / "app.yaml").read_text())
        self.assertNotIn("  header: custom-header", (config / "app.yaml").read_text())
        self.assertIn("otherSetting: retained", (config / "app.yaml").read_text())
        self.assertEqual(
            self._environment(),
            {
                "APP_CONFIG_PATH": str(config / "app.yaml"),
                "SERVERS_CONFIG_PATH": str(config / "mcp.json"),
                "AUDIT_LOG_DIR": str(data / "audit-logs"),
                "DIND_ENABLED": "false",
                "AUTH_KEY": "secret",
                "ALLOWED_IP_RANGES": "10.0.0.0/8,192.168.1.0/24",
                "CORS_ORIGINS": "https://one.example,https://two.example",
            },
        )
        self.assertTrue({f"chown:lunar:lunar:{path}" for path in (config, data, data / "audit-logs", config / "app.yaml", config / "mcp.json")}.issubset(self._log()))
        self.assertIn(f"node:lunar:{data}", self._log())

    def test_inserts_managed_header_when_existing_config_omits_it(self) -> None:
        config = self.root / "config"
        data = self.root / "data"
        config.mkdir()
        data.mkdir()
        (config / "app.yaml").write_text(
            "customSetting: retained\nauth:\n  enabled: false\notherSetting: retained\n"
        )

        result = self._run()

        self.assertEqual(result.returncode, 0, result.stderr)
        app_config = (config / "app.yaml").read_text()
        self.assertIn("auth:\n  header: x-lunar-api-key\n  enabled: false", app_config)
        self.assertIn("otherSetting: retained", app_config)

    def test_docker_disabled_starts_without_a_docker_socket(self) -> None:
        result = self._run(TEST_ENABLE_DOCKER_MCP="false")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("docker:lunar", self._log())
        self.assertEqual(self._environment()["DIND_ENABLED"], "false")
        self.assertIn("  enabled: false", (self.root / "config/app.yaml").read_text())
        self.assertIn("  header: x-lunar-api-key", (self.root / "config/app.yaml").read_text())
        self.assertEqual((self.root / "config/mcp.json").read_text(), '{\n  "mcpServers": {}\n}\n')

    def test_docker_enabled_without_socket_fails_before_starting_services(self) -> None:
        result = self._run(TEST_ENABLE_DOCKER_MCP="true")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error:Docker MCP support requires the Home Assistant Docker API. Disable Protection Mode and restart, or set enable_docker_mcp to false.", self._log())
        self.assertNotIn("generate:lunar", self._log())
        self.assertFalse(any(entry.startswith("node:lunar:") for entry in self._log()))

    def test_docker_enabled_with_inaccessible_api_fails_before_starting_services(self) -> None:
        self._start_socket()
        result = self._run(TEST_ENABLE_DOCKER_MCP="true", TEST_DOCKER_ACCESS="denied")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("docker:lunar", self._log())
        self.assertIn("error:Docker MCP support cannot access the Home Assistant Docker API as lunar. Disable Protection Mode and restart, or set enable_docker_mcp to false.", self._log())
        self.assertNotIn("generate:lunar", self._log())

    def test_docker_enabled_with_access_enables_docker_support(self) -> None:
        self._start_socket()
        result = self._run(TEST_ENABLE_DOCKER_MCP="true", TEST_DOCKER_ACCESS="ok")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("docker:lunar", self._log())
        self.assertIn("addgroup:lunar root", self._log())
        self.assertEqual(self._environment()["DIND_ENABLED"], "true")


class McpxReleaseContractTests(unittest.TestCase):
    """Cross-file release metadata and optional upstream patch validation."""

    def test_release_metadata_has_one_version_ref_image_and_architecture_set(self) -> None:
        config = (ADDON_DIR / "config.yaml").read_text()
        dockerfile = (ADDON_DIR / "Dockerfile").read_text()
        workflow = (REPO_ROOT / ".github/workflows/addon-mcpx.yml").read_text()
        changelog = (ADDON_DIR / "CHANGELOG.md").read_text()

        def capture(pattern: str, text: str) -> str:
            match = re.search(pattern, text, re.MULTILINE)
            self.assertIsNotNone(match, pattern)
            return match.group(1)

        version = capture(r'^version: "([^"]+)"$', config)
        self.assertEqual(version, capture(r'^  VERSION: ([^\n]+)$', workflow))
        self.assertEqual(version, capture(r'^ARG BUILD_VERSION=([^\n]+)$', dockerfile))
        self.assertIsNotNone(re.search(rf'^## {re.escape(version)}$', changelog, re.MULTILINE))

        ref = capture(r'^ARG MCPX_REF=([0-9a-f]+)$', dockerfile)
        patch = ADDON_DIR / "patches" / f"lunar-{ref}.patch"
        self.assertTrue(patch.is_file())
        self.assertEqual(patch.name, capture(r'^COPY patches/(lunar-[^ ]+\.patch) /tmp/$', dockerfile))

        image = capture(r'^image: "([^"]+)"$', config)
        registry = capture(r'^  REGISTRY_PREFIX: ([^\n]+)$', workflow)
        image_name = capture(r'^  IMAGE_NAME: ([^\n]+)$', workflow)
        self.assertEqual(image, f"{registry}/{image_name}")
        self.assertEqual(
            set(re.findall(r'^  - (aarch64|amd64)$', config, re.MULTILINE)),
            set(re.findall(r'"(aarch64|amd64)"', capture(r"^  ARCHITECTURES: '([^\n]+)'$", workflow))),
        )

    @unittest.skipUnless(os.environ.get("UPSTREAM_DIR"), "set UPSTREAM_DIR to the pinned Lunar source root")
    def test_patch_applies_cleanly_to_pinned_upstream(self) -> None:
        upstream = Path(os.environ["UPSTREAM_DIR"])
        self.assertTrue((upstream / "mcpx").is_dir(), "UPSTREAM_DIR must be the Lunar source root")
        ref = re.search(r"^ARG MCPX_REF=([0-9a-f]+)$", (ADDON_DIR / "Dockerfile").read_text(), re.MULTILINE)
        self.assertIsNotNone(ref)
        patch = ADDON_DIR / "patches" / f"lunar-{ref.group(1)}.patch"
        result = subprocess.run(
            ["patch", "--dry-run", "--fuzz=0", "--batch", "--forward", "-p1", "-d", str(upstream)],
            input=patch.read_text(),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
