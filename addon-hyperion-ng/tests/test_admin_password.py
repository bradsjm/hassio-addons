#!/usr/bin/env python3
"""Offline process-level checks for the Hyperion admin-password bootstrap.

Run directly with ``python3 addon-hyperion-ng/tests/test_admin_password.py``
after installing ``PyYAML==6.0.2`` (the version installed by CI). The suite
uses a loopback TCP server and temporary command/config shims; it never starts
Hyperion, Docker, or Home Assistant.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tempfile
import threading
import time
import unittest

try:
    import yaml
except ImportError as error:
    raise RuntimeError("Install PyYAML==6.0.2 to run the Hyperion add-on tests") from error


REPO_ROOT = Path(__file__).resolve().parents[2]
ADDON_DIR = REPO_ROOT / "addon-hyperion-ng"
RUN_SOURCE = ADDON_DIR / "run.sh"
API_ADDRESS = ("127.0.0.1", 19444)

FAKE_DAEMON = r'''#!/usr/bin/env bash
set -eu
printf 'started\n' > "${TEST_DAEMON_STARTED:?}"
trap 'printf "term\n" > "${TEST_DAEMON_TERMINATED:?}"; exit 0' TERM INT
while true; do sleep 0.05; done
'''


class FakeHyperionServer:
    """Minimal single-line JSON implementation of Hyperion's authorize API."""

    def __init__(self, *, new_password_required: bool, login_success: bool = True) -> None:
        self.new_password_required = new_password_required
        self.login_success = login_success
        self.connections: list[list[dict[str, object]]] = []
        self.errors: list[BaseException] = []
        self._stop = threading.Event()
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listener.bind(API_ADDRESS)
        self._listener.listen()
        self._listener.settimeout(0.05)
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def close(self) -> None:
        self._stop.set()
        self._listener.close()
        self._thread.join(timeout=2)
        if self._thread.is_alive():
            raise AssertionError("fake Hyperion server did not stop")
        if self.errors:
            raise self.errors[0]

    def wait_for_requests(self, count: int, timeout: float = 2) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if sum(map(len, self.connections)) >= count:
                return
            time.sleep(0.01)
        raise AssertionError(f"expected {count} requests, received {self.connections!r}")

    def _serve(self) -> None:
        try:
            while not self._stop.is_set():
                try:
                    connection, _ = self._listener.accept()
                except (OSError, TimeoutError):
                    continue
                with connection:
                    connection.settimeout(2)
                    requests: list[dict[str, object]] = []
                    self.connections.append(requests)
                    reader = connection.makefile("rb")
                    writer = connection.makefile("wb")
                    try:
                        for line in reader:
                            request = json.loads(line)
                            requests.append(request)
                            response = self._response_for(request)
                            writer.write(json.dumps(response, separators=(",", ":")).encode() + b"\n")
                            writer.flush()
                    finally:
                        reader.close()
                        writer.close()
        except BaseException as error:  # surfaced by close() in the test thread
            if not self._stop.is_set():
                self.errors.append(error)

    def _response_for(self, request: dict[str, object]) -> dict[str, object]:
        subcommand = request.get("subcommand")
        if subcommand == "newPasswordRequired":
            return {"success": True, "info": {"newPasswordRequired": self.new_password_required}}
        if subcommand == "login":
            return {"success": self.login_success}
        if subcommand == "newPassword":
            return {"success": True}
        raise AssertionError(f"unexpected authorize request: {request!r}")


class HyperionAdminPasswordTests(unittest.TestCase):
    """Administrator-password behavior observable at the runtime boundary."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.log = self.root / "bashio.log"
        self.daemon_started = self.root / "daemon.started"
        self.daemon_terminated = self.root / "daemon.terminated"
        self.server: FakeHyperionServer | None = None
        self.process: subprocess.Popen[str] | None = None

        self.daemon = self.root / "hyperiond"
        self.daemon.write_text(FAKE_DAEMON)
        self.daemon.chmod(0o755)
        self.run_copy = self.root / "run"
        self.run_copy.write_text(
            RUN_SOURCE.read_text()
            .replace("mkdir -p /config/hyperion", 'mkdir -p "${TEST_CONFIG_DIR:?}/hyperion"')
            .replace("/usr/bin/hyperiond", '"${TEST_HYPERIOND:?}"')
            .replace("for attempt in $(seq 1 15); do", "for attempt in $(seq 1 1); do")
            .replace("        sleep 1\n", "        sleep 0.01\n")
        )
        self.wrapper = self.root / "run-with-bashio"
        self.wrapper.write_text(
            """#!/usr/bin/env bash
bashio::config.has_value() { [[ -n \"${TEST_ADMIN_PASSWORD:-}\" ]]; }
bashio::config() { printf '%s' \"${TEST_ADMIN_PASSWORD:?}\"; }
bashio::log.info() { printf 'info:%s\\n' \"$*\" >> \"${TEST_BASHIO_LOG:?}\"; }
bashio::log.warning() { printf 'warning:%s\\n' \"$*\" >> \"${TEST_BASHIO_LOG:?}\"; }
bashio::log.error() { printf 'error:%s\\n' \"$*\" >> \"${TEST_BASHIO_LOG:?}\"; }
source \"${TEST_RUN_COPY:?}\"
"""
        )
        self.wrapper.chmod(0o755)

    def tearDown(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self._stop_runtime()
        if self.server is not None:
            self.server.close()
        self.tempdir.cleanup()

    def _start_server(self, **kwargs: object) -> FakeHyperionServer:
        self.server = FakeHyperionServer(**kwargs)
        self.server.start()
        return self.server

    def _start_runtime(self, password: str = "") -> None:
        environment = os.environ | {
            "TEST_ADMIN_PASSWORD": password,
            "TEST_BASHIO_LOG": str(self.log),
            "TEST_CONFIG_DIR": str(self.root / "config"),
            "TEST_HYPERIOND": str(self.daemon),
            "TEST_DAEMON_STARTED": str(self.daemon_started),
            "TEST_DAEMON_TERMINATED": str(self.daemon_terminated),
            "TEST_RUN_COPY": str(self.run_copy),
        }
        self.process = subprocess.Popen(
            ["bash", str(self.wrapper)],
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._wait_until(lambda: self.daemon_started.exists(), "daemon did not start")

    def _stop_runtime(self) -> subprocess.CompletedProcess[str]:
        assert self.process is not None
        self.process.send_signal(signal.SIGTERM)
        stdout, stderr = self.process.communicate(timeout=3)
        result = subprocess.CompletedProcess(self.process.args, self.process.returncode, stdout, stderr)
        self.assertEqual(result.returncode, 0, result.stderr)
        self._wait_until(lambda: self.daemon_terminated.exists(), "daemon did not receive TERM")
        self.process = None
        return result

    def _wait_until(self, predicate: object, failure: str, timeout: float = 2) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():  # type: ignore[operator]
                return
            time.sleep(0.01)
        self.fail(failure)

    def _logs(self) -> str:
        return self.log.read_text() if self.log.exists() else ""

    def test_config_declares_an_optional_masked_admin_password(self) -> None:
        config = yaml.safe_load((ADDON_DIR / "config.yaml").read_text())

        self.assertEqual(config["options"]["admin_password"], "")
        self.assertEqual(config["schema"]["admin_password"], "password?")

    def test_empty_option_skips_password_bootstrap(self) -> None:
        self._start_runtime()
        result = self._stop_runtime()

        self.assertEqual(self._logs(), "")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_short_password_does_not_connect_or_attempt_authentication(self) -> None:
        server = self._start_server(new_password_required=True)
        self._start_runtime("short")
        self._wait_until(lambda: "must contain at least 8 characters" in self._logs(), "short password was not rejected")
        self._stop_runtime()

        self.assertEqual(server.connections, [])
        self.assertIn("skipping password bootstrap", self._logs())

    def test_default_password_flow_rotates_on_one_connection(self) -> None:
        server = self._start_server(new_password_required=True)
        self._start_runtime("configured-password")
        server.wait_for_requests(3)
        self._wait_until(
            lambda: "Configured Hyperion admin password on initial startup" in self._logs(),
            "initial password bootstrap did not complete",
        )
        self._stop_runtime()

        self.assertEqual(len(server.connections), 1)
        self.assertEqual(
            server.connections[0],
            [
                {"command": "authorize", "subcommand": "newPasswordRequired"},
                {"command": "authorize", "subcommand": "login", "password": "hyperion"},
                {
                    "command": "authorize",
                    "subcommand": "newPassword",
                    "password": "hyperion",
                    "newPassword": "configured-password",
                },
            ],
        )
        self.assertIn("Configured Hyperion admin password on initial startup", self._logs())

    def test_configured_password_is_only_verified_after_initial_setup(self) -> None:
        server = self._start_server(new_password_required=False, login_success=True)
        self._start_runtime("configured-password")
        server.wait_for_requests(2)
        self._wait_until(
            lambda: "Configured Hyperion admin password is already active" in self._logs(),
            "configured password verification did not complete",
        )
        self._stop_runtime()

        self.assertEqual(
            server.connections,
            [[
                {"command": "authorize", "subcommand": "newPasswordRequired"},
                {"command": "authorize", "subcommand": "login", "password": "configured-password"},
            ]],
        )
        self.assertIn("already active", self._logs())

    def test_different_existing_password_is_never_rotated(self) -> None:
        server = self._start_server(new_password_required=False, login_success=False)
        self._start_runtime("configured-password")
        server.wait_for_requests(2)
        self._wait_until(
            lambda: "refusing to overwrite an existing password" in self._logs(),
            "failed password verification did not complete",
        )
        self._stop_runtime()

        requests = server.connections[0]
        self.assertEqual(sum(request["subcommand"] == "login" for request in requests), 1)
        self.assertNotIn("newPassword", [request["subcommand"] for request in requests])
        self.assertIn("refusing to overwrite an existing password", self._logs())

    def test_quoted_and_escaped_password_is_json_encoded_without_logging_the_secret(self) -> None:
        password = 'quote" and slash\\ password'
        server = self._start_server(new_password_required=True)
        self._start_runtime(password)
        server.wait_for_requests(3)
        self._wait_until(
            lambda: "Configured Hyperion admin password on initial startup" in self._logs(),
            "escaped password bootstrap did not complete",
        )
        result = self._stop_runtime()

        self.assertEqual(server.connections[0][2]["newPassword"], password)
        self.assertNotIn(password, self._logs())
        self.assertNotIn(password, result.stdout)
        self.assertNotIn(password, result.stderr)

    def test_readiness_timeout_is_non_fatal_and_runtime_forwards_term_to_daemon(self) -> None:
        self._start_runtime("configured-password")
        self._wait_until(lambda: "did not become ready" in self._logs(), "readiness failure was not logged")
        result = self._stop_runtime()

        self.assertIn("Hyperion will continue running", self._logs())
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
