# MCPX Server Add-on

MCPX provides an MCP gateway and browser control plane for MCP servers.

While MCPX supports any type of MCP server, this add-on is most often used to allow for a relatively safe way to run `stdio` type MCP servers in a container and invoke them via HTTP from other clients such as N8N and similar components.

## URLs

Use these URLs from your LAN, replacing `<ha-host>` with your Home Assistant host name or IP address:

- MCP client URL: `http://<ha-host>:9000/mcp`
- MCPX UI: `http://<ha-host>:5173`

## Configuration Files

The add-on creates these files on first start and never overwrites them after that:

- `/config/mcpx/app.yaml`
- `/config/mcpx/mcp.json`

Add native MCPX server definitions to `/config/mcpx/mcp.json`.

## Audit Logs

Audit logs are written under:

- `/data/mcpx/audit-logs`

## Metrics

Prometheus metrics are disabled by default.

To expose metrics:

1. Enable the `enable_metrics` option.
2. Map `3000/tcp` to a host port in the add-on network settings.
3. Open `http://<ha-host>:3000/metrics`.

With default settings, `/metrics` should not be reachable.

## Security

MCPX is exposed directly to your LAN on ports `9000` and `5173`.
Use `auth_key` and/or `allowed_ip_ranges` when exposing the add-on outside a trusted network.

## Unsupported

MCPX target servers using `"command": "docker"` are unsupported in this version. They should fail through MCPX's normal error path; the add-on does not start Docker, request privileged mode, or mount `/var/run/docker.sock`.
