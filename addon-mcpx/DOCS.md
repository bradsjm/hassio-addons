# MCPX Server Add-on

MCPX provides an MCP gateway and browser control plane for MCP servers.

While MCPX supports any type of MCP server, this add-on is most often used to allow for a relatively safe way to run `stdio` type MCP servers in a container and invoke them via HTTP from other clients such as N8N and similar components.

## URLs

Use these URLs from your LAN, replacing `<ha-host>` with your Home Assistant host name or IP address:

- MCP client URL: `http://<ha-host>:9000/mcp`
- MCPX UI: `http://<ha-host>:5173`

## Breaking migration from 0.1

Version 0.2.0 uses a new add-on-specific configuration folder and does not migrate old files. Before or after upgrading, manually move:

- `/config/mcpx/app.yaml` to `/config/app.yaml`
- `/config/mcpx/mcp.json` to `/config/mcp.json`

There is no compatibility mapping or automated migration. Stop the add-on while moving the files.

## Configuration Files

The add-on creates missing configuration files:

- `/config/app.yaml`
- `/config/mcp.json`

Add native MCPX server definitions to `/config/mcp.json`. Existing server definitions are preserved. At each startup, the add-on synchronizes `auth.enabled` in `/config/app.yaml` with the `auth_key` option and enforces `auth.header: x-lunar-api-key` for the browser REST and Socket.IO clients.

## Audit Logs

Audit logs are written under:

- `/data/audit-logs`

MCPX also keeps token and relative `.mcpx` state in `/data`.

The multi-architecture add-on image is distributed as `docker.io/bradsjm/addon-mcpx`.

## Metrics

Prometheus metrics are disabled by default.

To expose metrics:

1. Enable the `enable_metrics` option.
2. Map `3000/tcp` to a host port in the add-on network settings.
3. Open `http://<ha-host>:3000/metrics`.

With default settings, `/metrics` should not be reachable.

## Security

MCPX is exposed directly to your LAN on ports `9000` and `5173`. `auth_key` is optional. When configured, the browser UI prompts for it, sends it as `x-lunar-api-key` for REST calls, and includes it in the Socket.IO handshake. `allowed_ip_ranges` applies to both REST and Socket.IO connections.

Set `cors_origins` to restrict browser origins. With no configured origins, MCPX reflects the requesting origin rather than returning a wildcard with credentials.

## Docker MCP servers

`enable_docker_mcp` is disabled by default. When enabled, it allows trusted server definitions to use the host Docker API directly. The add-on installs the Docker CLI only: it does not start Docker-in-Docker or use another add-on. Home Assistant makes this API available only outside Protection Mode; startup checks access as the unprivileged `lunar` user and otherwise instructs you to disable Protection Mode or turn the option off.

Access to the host Docker API is effectively host-root access. Enable it only for trusted MCP server definitions and clients.
