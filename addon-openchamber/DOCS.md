# Home Assistant Add-on: OpenChamber

[OpenChamber](https://openchamber.dev/) is a rich web interface for the [OpenCode](https://opencode.ai/) AI coding assistant. It provides a visual alternative to the command line with chat branching, diff viewing, multi-agent runs, git integration, and a mobile-friendly PWA.

This add-on runs the OpenChamber web UI directly inside Home Assistant. In managed mode (default), it also runs OpenCode behind the scenes — the full stack in one container.

## Home Assistant Integration

In managed mode, this add-on automatically installs [ha-mcp](https://github.com/homeassistant-ai/ha-mcp), enabling OpenCode to communicate with your Home Assistant instance locally. This allows OpenCode to interact with your Home Assistant entities, automations, and other Home Assistant features without requiring external API access.

## App configuration

You can configure the add-on through the **Configuration** tab in the add-on panel.

### Port

The port on which the OpenChamber web UI listens. The default is `3000`.

### OpenCode mode

- **managed** (default): The add-on installs and runs OpenCode internally. OpenChamber connects to this managed instance automatically. This is the recommended mode for most users.
- **external**: OpenChamber connects to an existing OpenCode server (e.g. the [OpenCode add-on](https://github.com/bradsjm/hassio-addons)). You must provide the `opencode_host` and optionally `opencode_port`.

### External OpenCode host / port

When mode is `external`, set the URL of the running OpenCode server (e.g. `http://192.168.1.100:4096`). The port defaults to `4096`.

### UI password

A single shared password to protect the OpenChamber web UI. Leave empty for no authentication (not recommended for exposed networks).

### Version pins

- **OpenCode version pin**: Pin OpenCode to a specific version (e.g. `0.6.0`). Only used in managed mode. Leave empty to install latest.
- **OpenChamber version pin**: Pin OpenChamber to a specific version (e.g. `1.9.10`). Leave empty to install latest.

### OpenCode environment variables

Use this option to set additional `OPENCODE_` environment variables before OpenCode starts. Enter each item as `KEY=value` (e.g. `OPENCODE_DISABLE_LSP_DOWNLOAD=true`). Only variables prefixed with `OPENCODE_` are accepted.

## Accessing the Web Interface

After starting the add-on:

1. Open your web browser and navigate to `http://<home-assistant-host>:3000`
2. If a password is configured, enter it at the login prompt
3. You can now interact with OpenCode through the OpenChamber web interface

## Support

If you encounter issues with this add-on:

- Check the **Log** tab in the add-on panel for error messages
- Ensure the configured port is not in use by another service
- For OpenChamber-specific issues, visit the [OpenChamber GitHub repository](https://github.com/openchamber/openchamber)
- For OpenCode-specific issues, visit the [OpenCode documentation](https://opencode.ai/docs/)
