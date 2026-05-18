# Home Assistant Add-on: MCPX Server

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[![GitHub Activity][commits-shield]][commits]

_MCP gateway and browser control plane for Home Assistant._

## About

[MCPX](https://github.com/TheLunarCompany/lunar/tree/main/mcpx) provides an MCP gateway and browser control plane for MCP servers.

This add-on is most often used to run `stdio` type MCP servers in a container and invoke them over HTTP from other clients such as n8n and similar components.

The MCP client URL is `http://<ha-host>:9000/mcp`, and the MCPX UI is available at `http://<ha-host>:5173`.

## Configuration

The add-on creates these files on first start and never overwrites them after that:

- `/config/mcpx/app.yaml`
- `/config/mcpx/mcp.json`

Add native MCPX server definitions to `/config/mcpx/mcp.json`.

Audit logs are written to `/data/mcpx/audit-logs`.

Prometheus metrics are disabled by default. To expose metrics, enable the `enable_metrics` option, map `3000/tcp` to a host port in the add-on network settings, and open `http://<ha-host>:3000/metrics`.

## Security

MCPX is exposed directly to your LAN on ports `9000` and `5173`. Use `auth_key` and/or `allowed_ip_ranges` when exposing the add-on outside a trusted network.

## Unsupported

MCPX target servers using `"command": "docker"` are unsupported in this version. They should fail through MCPX's normal error path; the add-on does not start Docker, request privileged mode, or mount `/var/run/docker.sock`.

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
