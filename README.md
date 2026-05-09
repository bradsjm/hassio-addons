# Jonathan's Home Assistant Add-Ons

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[![GitHub Activity][commits-shield]][commits]

_A collection of Home Assistant add-ons for Hyperion.NG, OpenCode, and OpenChamber._

## About

This repository provides Home Assistant add-ons that extend your smart home with ambient lighting, AI coding assistance, and rich web interfaces.

## Add-ons provided by this repository

### [OpenChamber][addon-openchamber]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

Rich web interface for the OpenCode AI coding agent with chat branching, diff viewing, multi-agent runs, git integration, and a mobile-friendly PWA. Runs the full stack in one container — OpenCode backend and OpenChamber frontend.

[:books: OpenChamber documentation][doc-openchamber]

### [OpenCode Server][addon-opencode]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

OpenCode web server configured for Home Assistant. Provides a web UI or headless API server for AI-powered coding assistance, with automatic Home Assistant integration via MCP.

[:books: OpenCode documentation][doc-opencode]

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

## Support

Got questions?

- [Open an issue on GitHub][issue]

## License

MIT License

Copyright (c) 2021-2026 Jonathan Bradshaw

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[addon-hyperion]: https://github.com/bradsjm/hassio-addons/tree/main/addon-hyperion-ng
[addon-opencode]: https://github.com/bradsjm/hassio-addons/tree/main/addon-opencode
[addon-openchamber]: https://github.com/bradsjm/hassio-addons/tree/main/addon-openchamber
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/m/bradsjm/hassio-addons.svg
[commits]: https://github.com/bradsjm/hassio-addons/commits/main
[doc-hyperion]: https://github.com/bradsjm/hassio-addons/blob/main/addon-hyperion-ng/README.md
[doc-opencode]: https://github.com/bradsjm/hassio-addons/blob/main/addon-opencode/DOCS.md
[doc-openchamber]: https://github.com/bradsjm/hassio-addons/blob/main/addon-openchamber/DOCS.md
[issue]: https://github.com/bradsjm/hassio-addons/issues
[license-shield]: https://img.shields.io/github/license/bradsjm/hassio-addons.svg
[releases-shield]: https://img.shields.io/github/release/bradsjm/hassio-addons/all.svg
[releases]: https://github.com/bradsjm/hassio-addons/releases
[repository-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fbradsjm%2Fhassio-addons
