# Hyperion.NG Add-on Guidance

## Structure

- `config.yaml` defines the 2.2.1 add-on metadata for `amd64` and `aarch64`.
- `Dockerfile` uses the explicitly pinned multi-architecture base `ghcr.io/home-assistant/base-debian:bookworm-2026.06.0`.
- `download-hyperion.sh` maps Home Assistant architectures to the exact upstream archive names and validates downloads before extraction.
- `run.sh` must remain a root entrypoint and store persistent configuration in `/config/hyperion`.

## Releases and Builds

- The generic published image is `docker.io/bradsjm/addon-hyperion-ng`.
- The GitHub Actions workflow builds supported architectures with `home-assistant/builder` composite actions and publishes the multi-architecture manifest only on pushes to `master`.
- When updating the version, verify both upstream `Linux-amd64` and `Linux-arm64` archives. The manual `update-hyperion-version.sh` helper validates them before changing `config.yaml`.
- Preserve the required runtime packages and build-time `hyperiond --version` and `ldd` checks. Hyperion's archive provides its bundled libraries.

## Runtime Contract

- Host networking exposes Hyperion's fixed listeners directly; the Web UI is `http://<host>:8090`. Resolve any host port conflicts before starting the add-on.
- `admin_password` bootstraps only Hyperion's initial default password; preserve the refusal to replace an existing non-default password.
- Preserve the existing privileged capabilities, UART/USB/video/GPIO settings, and device declarations.
- Required device paths include video devices (`/dev/fb0`, `/dev/amvideo`, `/dev/vchiq`), SPI (`/dev/spidev0.0`), and memory (`/dev/mem`).
