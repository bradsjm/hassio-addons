# Home Assistant Add-on: OpenCode

OpenCode is an AI-powered coding assistant that helps you write, understand, and debug code. It can analyze your codebase, suggest improvements, explain complex code, and help with debugging tasks—similar to tools like Cursor or GitHub Copilot, but designed for command-line use.

This add-on runs the OpenCode web server or headless API server directly inside Home Assistant, providing local access to OpenCode's capabilities from within your home network.

## Home Assistant Integration

This add-on automatically installs [ha-mcp](https://github.com/homeassistant-ai/ha-mcp), enabling OpenCode to communicate with your Home Assistant instance locally. This integration allows OpenCode to interact with your Home Assistant entities, automations, and other Home Assistant features without requiring external API access.

## App configuration

You can configure the add-on through the **Configuration** tab in the add-on panel.

### Port

The port on which OpenCode listens. The default is `4096`.

Make sure the port is not used by another service on your Home Assistant instance.

### Username

The username for HTTP basic authentication. The default is `opencode`. Authentication is only enforced when a password is set.

### Password

The password for HTTP basic authentication. Leave empty to disable authentication (not recommended for exposed networks). When set, both the web UI and API require this username and password for access.

### OpenCode version pin

Set this to a specific OpenCode version (for example `0.6.0`) to pin the add-on to that release. Leave it empty to install the latest OpenCode release on every startup.

OpenCode configuration files are stored in `/config/opencode`. The OpenCode binary and runtime data are stored under `/data`.

### OpenCode environment variables

Use this option to set additional `OPENCODE_` environment variables before OpenCode starts.

Enter each item as `KEY=value` (for example `OPENCODE_DISABLE_LSP_DOWNLOAD=true` or `OPENCODE_MODELS_URL=https://example.com/models.json`).

Only variables prefixed with `OPENCODE_` are accepted.

## Accessing the Web Interface

After starting the add-on:

1. Open your web browser and navigate to `http://<home-assistant-host>:4096` (replace `<home-assistant-host>` with your Home Assistant IP address or hostname).
2. If authentication is configured, enter the username and password you set in the add-on configuration.
3. You can now interact with OpenCode through the web interface.
4. See [Opencode Web Documentation](https://opencode.ai/docs/web/) for more details.

## Attaching a Terminal

You can attach a terminal TUI to a running web server:

```bash
# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Connect to Home Assistant instance
opencode attach http://homeassistant.local:4096
```

## Support

If you encounter issues with this add-on:

- Check the **Log** tab in the add-on panel for error messages.
- Ensure the configured port is not in use by another service.
- Verify your network settings and firewall rules allow access to the configured port.
- For Home Assistant-specific issues, visit the [Home Assistant Community Forum](https://community.home-assistant.io).
- For OpenCode-specific issues, visit the [OpenCode documentation](https://opencode.ai/docs/) or [GitHub repository](https://github.com/anomalyco/opencode).
