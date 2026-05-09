# Home Assistant Add-on: OpenChamber

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[![GitHub Activity][commits-shield]][commits]

_Rich web interface for the OpenCode AI coding agent._

## About

[OpenChamber](https://openchamber.dev/) is a rich web interface for [OpenCode](https://opencode.ai/) with chat branching, diff viewing, multi-agent runs, git integration, and a mobile-friendly PWA. It provides a visual alternative to the command line — use OpenCode from any browser on any device.

This add-on runs the full stack in one container. In managed mode (default), it runs both the OpenCode backend and the OpenChamber frontend. It can also connect to an existing OpenCode server.

This add-on automatically installs [ha-mcp](https://github.com/homeassistant-ai/ha-mcp) in managed mode, enabling OpenCode to communicate with your Home Assistant instance.

[:books: Read the full add-on documentation][docs]

## Support

Got questions?

- [Open an issue on GitHub][issue]

## We have got some Home Assistant add-ons for you

Want some more functionality to your Home Assistant instance?

Check out the [Jonathan's Home Assistant Add-Ons][repository] repository for additional add-ons.

## License

MIT License

Copyright (c) 2026 Jonathan Bradshaw

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/m/bradsjm/hassio-addons.svg
[commits]: https://github.com/bradsjm/hassio-addons/commits/main
[docs]: https://github.com/bradsjm/hassio-addons/blob/main/addon-openchamber/DOCS.md
[issue]: https://github.com/bradsjm/hassio-addons/issues
[license-shield]: https://img.shields.io/github/license/bradsjm/hassio-addons.svg
[releases-shield]: https://img.shields.io/github/release/bradsjm/hassio-addons/all.svg
[releases]: https://github.com/bradsjm/hassio-addons/releases
[repository]: https://github.com/bradsjm/hassio-addons
