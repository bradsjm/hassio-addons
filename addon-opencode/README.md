# Home Assistant Add-on: OpenCode

_OpenCode web server for Home Assistant._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

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
