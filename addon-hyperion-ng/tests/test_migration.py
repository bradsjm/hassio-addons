#!/usr/bin/env python3
"""Offline behavior checks for the Hyperion.NG 2.2.1 builder migration.

Run directly with ``python3 addon-hyperion-ng/tests/test_migration.py`` after
installing ``PyYAML==6.0.2`` (the version installed by CI). The tests replace
curl at the process boundary, so they require neither Docker nor network
access.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

try:
    import yaml
except ImportError as error:
    raise RuntimeError("Install PyYAML==6.0.2 to run the Hyperion add-on tests") from error


REPO_ROOT = Path(__file__).resolve().parents[2]
ADDON_DIR = REPO_ROOT / "addon-hyperion-ng"
CONFIG_FILE = ADDON_DIR / "config.yaml"
TRANSLATIONS_FILE = ADDON_DIR / "translations/en.yaml"
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

UPDATE_CURL_SUCCESS = r'''#!/usr/bin/env python3
import os
from pathlib import Path
import sys

url = sys.argv[-1]
with Path(os.environ["CURL_LOG"]).open("a") as log:
    log.write(url + "\n")

if url.endswith("/releases/latest"):
    print('{"tag_name":"2.2.2"}')
    raise SystemExit(0)
if url.endswith("Hyperion-2.2.2-Linux-amd64.tar.gz") or url.endswith("Hyperion-2.2.2-Linux-arm64.tar.gz"):
    raise SystemExit(0)
raise SystemExit("unexpected curl URL: " + url)
'''


class HyperionMigrationTests(unittest.TestCase):
    """Public downloader, update-helper, and add-on metadata contracts."""

    def _make_executable(self, directory: Path, name: str, contents: str) -> Path:
        executable = directory / name
        executable.write_text(contents)
        executable.chmod(0o755)
        return executable

    def _write_config_fixture(self, workspace: Path) -> tuple[Path, str]:
        config_dir = workspace / "addon-hyperion-ng"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        contents = CONFIG_FILE.read_text().replace('version: "2.2.1"', 'version: "2.0.16"', 1)
        config_file.write_text(contents)
        return config_file, contents

    def _run_update_helper(
        self, workspace: Path, curl_script: str
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        bin_dir = workspace / "bin"
        bin_dir.mkdir()
        self._make_executable(bin_dir, "curl", curl_script)
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
        return result, curl_log

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
            config_file, before = self._write_config_fixture(workspace)
            result, curl_log = self._run_update_helper(workspace, UPDATE_CURL)

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

    def test_update_helper_atomically_replaces_only_the_top_level_yaml_version(self) -> None:
        """A validated release replaces the version line without changing metadata."""
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = Path(tempdir)
            config_file, before = self._write_config_fixture(workspace)
            before_inode = config_file.stat().st_ino
            result, curl_log = self._run_update_helper(workspace, UPDATE_CURL_SUCCESS)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual(config_file.stat().st_ino, before_inode)
            self.assertEqual(
                config_file.read_text(),
                before.replace('version: "2.0.16"', 'version: "2.2.2"', 1),
            )
            updated = yaml.safe_load(config_file.read_text())
            expected = yaml.safe_load(before)
            expected["version"] = "2.2.2"
            self.assertEqual(updated, expected)
            self.assertEqual(list(config_file.parent.glob("config.yaml.tmp.*")), [])
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
        config = yaml.safe_load(CONFIG_FILE.read_text())

        self.assertTrue(CONFIG_FILE.is_file())
        self.assertFalse((ADDON_DIR / "config.json").exists())
        self.assertEqual(config["version"], "2.2.1")
        self.assertEqual(config["arch"], ["amd64", "aarch64"])
        self.assertIs(config["host_network"], True)
        self.assertEqual(config["image"], "docker.io/bradsjm/addon-hyperion-ng")
        self.assertEqual(config["webui"], "http://[HOST]:[PORT:8090]")
        self.assertNotIn("ports", config)
        self.assertNotIn("ports_description", config)

    def test_admin_password_translation_explains_the_safe_bootstrap_contract(self) -> None:
        """The configuration UI documents the password bootstrap safeguards."""
        translations = yaml.safe_load(TRANSLATIONS_FILE.read_text())
        admin_password = translations["configuration"]["admin_password"]

        self.assertEqual(admin_password["name"], "Admin password")
        description = admin_password["description"]
        self.assertIn("minimum 8 characters", description)
        self.assertIn("default password", description)
        self.assertIn("initial startup", description)
        self.assertIn("existing non-default password is not overwritten", description)

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
