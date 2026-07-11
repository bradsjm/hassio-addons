## About

This repository provides Home Assistant add-ons that extend your smart home with ambient lighting, AI coding assistance, rich web interfaces, and MCP server control.

## Add-ons provided by this repository

### [MCPX Server][addon-mcpx]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

MCP gateway and browser control plane for MCP servers, including optional direct host Docker API support for trusted server definitions.

[:books: MCPX documentation][doc-mcpx]

### [Hyperion.NG][addon-hyperion]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

Hyperion is an open-source bias and ambient lighting implementation that synchronizes LEDs with your screen content for immersive home theater and gaming experiences.

## Installation

[![Add repository on my Home Assistant][repository-badge]][repository-url]

To add this repository to your Home Assistant instance:

1. In the Home Assistant sidebar, click **Settings** → **Add-ons** → **Add-on store**
2. Click the **⋮** in the top-right corner and select **Repositories**
3. Enter `https://github.com/bradsjm/hassio-addons` and click **Add**
4. Find the desired add-on and click **Install**

For detailed instructions, see the [official Home Assistant documentation](https://www.home-assistant.io/common-tasks/supervised/#installing-third-party-add-ons).

## License

MIT License

Copyright (c) 2021-2026 Jonathan Bradshaw

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[addon-hyperion]: https://github.com/bradsjm/hassio-addons/tree/main/addon-hyperion-ng
[addon-mcpx]: https://github.com/bradsjm/hassio-addons/tree/main/addon-mcpx
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[doc-hyperion]: https://github.com/bradsjm/hassio-addons/blob/main/addon-hyperion-ng/README.md
[doc-mcpx]: https://github.com/bradsjm/hassio-addons/blob/main/addon-mcpx/DOCS.md
[license-shield]: https://img.shields.io/github/license/bradsjm/hassio-addons.svg
[repository-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fbradsjm%2Fhassio-addons
