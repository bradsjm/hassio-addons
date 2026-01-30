# Home Assistant Add-on: OpenCode

OpenCode is an AI-powered coding assistant that helps you write, understand, and debug code. It can analyze your codebase, suggest improvements, explain complex code, and help with debugging tasks—similar to tools like Cursor or GitHub Copilot, but designed for command-line use.

This add-on runs the OpenCode web server or headless API server directly inside Home Assistant, providing local access to OpenCode's capabilities from within your home network.

## Installation

The Home Assistant Add-ons repository is available via the official Home Assistant Supervisor. To install this add-on:

1. In the Home Assistant sidebar, click **Settings** → **Add-ons** → **Add-on store**.
2. Click the **⋮** (three dots) in the top-right corner and select **Add repository**.
3. Enter `https://github.com/bradsjm/hassio-addons` and click **Add**.
4. Find the "OpenCode" add-on in the repository list and click it.
5. Click **Install**.
6. After installation, start the add-on from the **Info** tab.

The add-on will be available at `http://<home-assistant-host>:4096` (or your configured port).

## App configuration

You can configure the add-on through the **Configuration** tab in the add-on panel.

### Port

The port on which OpenCode listens. The default is `4096`.

Make sure the port is not used by another service on your Home Assistant instance.

### Username

The username for HTTP basic authentication. The default is `opencode`. Authentication is only enforced when a password is set.

### Password

The password for HTTP basic authentication. Leave empty to disable authentication (not recommended for exposed networks). When set, both the web UI and API require this username and password for access.

### Auto update

When enabled, the add-on checks for a new OpenCode release on startup and installs it to `/config/opencode/bin/opencode`. If an update fails, the add-on continues using the bundled binary.

## Accessing the Web Interface

After starting the add-on:

1. Open your web browser and navigate to `http://<home-assistant-host>:4096` (replace `<home-assistant-host>` with your Home Assistant IP address or hostname).
2. If authentication is configured, enter the username and password you set in the add-on configuration.
3. You can now interact with OpenCode through the web interface.

## Support

If you encounter issues with this add-on:

- Check the **Log** tab in the add-on panel for error messages.
- Ensure the configured port is not in use by another service.
- Verify your network settings and firewall rules allow access to the configured port.
- For Home Assistant-specific issues, visit the [Home Assistant Community Forum](https://community.home-assistant.io).
- For OpenCode-specific issues, visit the [OpenCode documentation](https://opencode.ai/docs/) or [GitHub repository](https://github.com/anomalyco/opencode).
