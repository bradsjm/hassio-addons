# MCPX 0.2.0 BuildKit remediation

## Objective

Deliver the experimental MCPX Home Assistant add-on as version 0.2.0 with a pinned Lunar source tree, durable Home Assistant storage, optional direct host Docker API access, browser authentication fixes, and BuildKit-based Docker Hub publication.

## Decisions

- Lunar is pinned to verified commit `e4a70047221fa015973d78858b7bdfd7ca321b32`; no branch ref is used by the Dockerfile.
- `/config` is the writable `addon_config` mapping and contains only `/config/app.yaml` and `/config/mcp.json`. Mutable state, audit logs, and Lunar's relative `.mcpx` state remain under `/data`; the server starts with `/data` as its working directory. On every startup, the add-on synchronizes `auth.enabled` and enforces `auth.header: x-lunar-api-key` so Lunar REST, the browser UI, and Socket.IO use the same key name.
- `ENABLE_STDIO_MCP_SERVERS=true` is always exported. `VERSION` and `INSTANCE_ID` are initialized in the add-on service, which intentionally does not invoke Lunar's Docker-in-Docker entrypoint. The service starts UI and server as `lunar`, waits for the server, and always stops and reaps the UI.
- `enable_docker_mcp` defaults to false. When enabled, the service validates the Supervisor-provided host Docker socket and `docker version` as `lunar`, dynamically grants the socket group where needed, and sets `DIND_ENABLED=true`. It otherwise sets `DIND_ENABLED=false`. The image installs `docker-cli` only.
- The tracked Lunar patch is applied with `patch --batch --forward`; it fails on source drift. It allows the `x-lunar-api-key` REST header, reflects origins when no explicit CORS list is configured (never wildcard plus credentials), supplies/retries browser credentials, enforces the same Socket.IO handshake key, enforces socket IP ranges, and permits an empty relative UI server URL.
- The image is published as `docker.io/bradsjm/addon-mcpx`. The MCPX workflow uses Home Assistant builder actions `2026.06.0`; PR, manual, and non-main-push runs build without logging in or publishing, while main pushes use the existing Docker Hub credentials to publish per-architecture images and their manifest.

## Exact changed files

- `addon-mcpx/config.yaml`
- `addon-mcpx/Dockerfile`
- `addon-mcpx/rootfs/etc/services.d/mcpx/run`
- `addon-mcpx/README.md`
- `addon-mcpx/DOCS.md`
- `addon-mcpx/CHANGELOG.md`
- `addon-mcpx/translations/en.yaml`
- `addon-mcpx/patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch`
- `addon-mcpx/tests/verify.sh`
- `addon-mcpx/tests/test_runtime.py`
- `.github/workflows/addon-mcpx.yml`
- `README.md`
- Deleted: `addon-mcpx/build.yaml`
- Deleted: `.github/scripts/build-mcpx.sh`

## Migration note

`addon-mcpx/build.yaml` and `.github/scripts/build-mcpx.sh` are removed. Dockerfile defaults and labels replace build metadata, while the workflow builds generic multi-architecture Docker Hub images with BuildKit. This release is a breaking manual migration: move `/config/mcpx/app.yaml` and `/config/mcpx/mcp.json` into the new add-on-specific `/config/app.yaml` and `/config/mcp.json` paths; no compatibility mapping or automated migration is provided.

## Validation

The workflow validation job runs `addon-mcpx/tests/verify.sh` and `python3 addon-mcpx/tests/test_runtime.py` before architecture builds. To also verify the Lunar patch against a checkout of the pinned commit, run `UPSTREAM_DIR=/path/to/lunar addon-mcpx/tests/verify.sh`. The Docker build applies the patch and compiles the patched server and UI.
