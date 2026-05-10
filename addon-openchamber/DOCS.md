# Home Assistant Add-on: OpenChamber

[OpenChamber](https://openchamber.dev/) is a rich web interface for the [OpenCode](https://opencode.ai/) AI coding assistant. It provides a visual alternative to the command line with chat branching, diff viewing, multi-agent runs, git integration, and a mobile-friendly PWA.

This add-on runs the OpenChamber web UI directly inside Home Assistant. In managed mode (default), it also runs OpenCode behind the scenes — the full stack in one container.

## Home Assistant Integration

In managed mode, this add-on automatically installs [ha-mcp](https://github.com/homeassistant-ai/ha-mcp), enabling OpenCode to communicate with your Home Assistant instance locally. This allows OpenCode to interact with your Home Assistant entities, automations, and other Home Assistant features without requiring external API access.

## App configuration

You can configure the add-on through the **Configuration** tab in the add-on panel. If you expose the OpenCode port (see below), the port mapping must be set on the **Network** tab by assigning a host port to `4096/tcp`.

### Shared password

A single shared password applied to both the OpenChamber web UI and the managed OpenCode server. OpenCode server auth uses the hardcoded username `opencode`. Leave empty for no authentication (not recommended for exposed networks).

### OpenChamber options

**port**: The port on which the OpenChamber web UI listens. Default is `3000`.

**version pin**: Pin OpenChamber to a specific version (e.g. `1.9.10`). Leave empty to install the latest release.

**data_dir**: Persistent storage directory for OpenChamber data. Default is `/data/openchamber`.

### OpenCode options

**mode**:
- `managed` (default): The add-on installs and runs OpenCode internally. OpenChamber connects to this managed instance automatically.
- `external`: OpenChamber connects to an existing OpenCode server (e.g. the [OpenCode add-on](https://github.com/bradsjm/hassio-addons)). You must provide the `host` and optionally `port`.

**host**: When mode is `external`, the full URL of the running OpenCode server (e.g. `http://192.168.1.100:4096`).

**port**: The port OpenCode listens on. In managed mode this is the internal port (default `4096`). In external mode this is the remote server port.

**expose**: When `true`, the managed OpenCode server binds to `0.0.0.0:4096`, allowing external clients to connect directly. Requires the `4096/tcp` port mapping to be set on the Network tab. Default is `false`.

**version pin**: Pin OpenCode to a specific version (e.g. `0.6.0`). Only used in managed mode. Leave empty to install latest.

**env_vars**: Set additional `OPENCODE_` environment variables before OpenCode starts. Enter each item as `KEY=value` (e.g. `OPENCODE_DISABLE_LSP_DOWNLOAD=true`). Only variables prefixed with `OPENCODE_` are accepted.

**config_dir**: Directory for OpenCode configuration files. Default is `/config/opencode`.

**state_dir**: Directory for OpenCode runtime state (binary, cache, home). Default is `/data/opencode`.

### System options

**packages**: Additional Ubuntu packages to install on startup (e.g. `htop`, `nmap`).

**init_commands**: Shell commands to execute on startup before launching OpenChamber.

## Accessing the Web Interface

After starting the add-on:

1. Open your web browser and navigate to `http://<home-assistant-host>:3000`
2. If a password is configured, enter it at the login prompt
3. You can now interact with OpenCode through the OpenChamber web interface

To access the OpenCode API directly from external clients, enable `opencode.expose` in the Configuration tab and assign a host port to `4096/tcp` in the Network tab.

## Support

If you encounter issues with this add-on:

- Check the **Log** tab in the add-on panel for error messages
- Ensure the configured port is not in use by another service
- For OpenChamber-specific issues, visit the [OpenChamber GitHub repository](https://github.com/openchamber/openchamber)
- For OpenCode-specific issues, visit the [OpenCode documentation](https://opencode.ai/docs/)
