# Home Assistant Add-on: MCPX Server

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[![GitHub Activity][commits-shield]][commits]

_MCP gateway and browser control plane for Home Assistant._

## About

[MCPX](https://github.com/TheLunarCompany/lunar/tree/e4a70047221fa015973d78858b7bdfd7ca321b32/mcpx) provides an MCP gateway and browser control plane for MCP servers.

This add-on is most often used to run `stdio` type MCP servers in a container and invoke them over HTTP from other clients such as n8n and similar components.

The MCP client URL is `http://<ha-host>:9000/mcp`, and the MCPX UI is available at `http://<ha-host>:5173`.

## Breaking migration from 0.1

Version 0.2.0 uses a new add-on-specific configuration folder and does not migrate old files. Before or after upgrading, manually move the files from the former `mcpx/` folder into the new folder:

- `/config/mcpx/app.yaml` to `/config/app.yaml`
- `/config/mcpx/mcp.json` to `/config/mcp.json`

There is no compatibility mapping or automated migration. Stop the add-on while moving the files.

## Configuration

The add-on creates missing configuration files:

- `/config/app.yaml`
- `/config/mcp.json`

Add native MCPX server definitions to `/config/mcp.json`. Existing server definitions are preserved. At each startup, the add-on synchronizes `auth.enabled` in `/config/app.yaml` with the `auth_key` option and enforces `auth.header: x-lunar-api-key` for the browser REST and Socket.IO clients.

Audit logs, token state, and upstream relative `.mcpx` state are written under `/data`.

Prometheus metrics are disabled by default. To expose metrics, enable the `enable_metrics` option, map `3000/tcp` to a host port in the add-on network settings, and open `http://<ha-host>:3000/metrics`.

The multi-architecture add-on image is distributed as `docker.io/bradsjm/addon-mcpx`.

## Security

MCPX is exposed directly to your LAN on ports `9000` and `5173`. `auth_key` is optional; when set, the browser UI prompts for it and uses the `x-lunar-api-key` header for REST and the Socket.IO handshake. Configure `cors_origins` to restrict browser origins; when empty, MCPX reflects the requesting origin so credentials are never combined with a wildcard origin. `allowed_ip_ranges` applies to REST and Socket.IO connections.

## Docker MCP servers

Set `enable_docker_mcp` only when a server definition needs the host Docker API. It is disabled by default. The add-on installs only the Docker CLI and never starts Docker-in-Docker or depends on another add-on. Enabling it requires Home Assistant's Docker API, which is unavailable in Protection Mode; startup fails with instructions to disable Protection Mode or turn the option off.

Docker API access exposes host-root-equivalent control through the Docker daemon. Enable it only for trusted MCP server definitions and clients.

## Support

Got questions?

- [Open an issue on GitHub][issue]

## We have got some Home Assistant add-ons for you

Want some more functionality to your Home Assistant instance?

Check out the [Jonathan's Home Assistant Add-Ons][repository] repository for additional add-ons.

## License

MIT License

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/m/bradsjm/hassio-addons.svg
[commits]: https://github.com/bradsjm/hassio-addons/commits/main
[issue]: https://github.com/bradsjm/hassio-addons/issues
[license-shield]: https://img.shields.io/github/license/bradsjm/hassio-addons.svg
[releases-shield]: https://img.shields.io/github/release/bradsjm/hassio-addons/all.svg
[releases]: https://github.com/bradsjm/hassio-addons/releases
[repository]: https://github.com/bradsjm/hassio-addons
