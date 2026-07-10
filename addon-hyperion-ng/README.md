# Home Assistant Add-on: Hyperion.NG

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[![GitHub Activity][commits-shield]][commits]

_Open-source bias and ambient lighting for Home Assistant._

## About

[Hyperion.NG](https://hyperion-project.org/) is an open-source ambient lighting implementation that synchronizes LEDs with your screen content. It creates immersive bias lighting effects for home theater, gaming, and general ambiance by capturing screen colors and driving LED strips in real time.

This add-on provides hardware-privileged access to video devices, SPI interfaces, and USB controllers for direct LED strip control from within Home Assistant.

## Admin password

Optionally set `admin_password` in the add-on configuration to bootstrap Hyperion's administrator password on its first start. Hyperion requires at least 8 characters. The add-on only changes the initial default password; if Hyperion already has a different password, it verifies the configured value and refuses to overwrite it when it does not match.

## Support

Got questions?

- [Hyperion Project Forum](https://hyperion-project.org/)
- [Open an issue on GitHub][issue]

## We have got some Home Assistant add-ons for you

Want some more functionality to your Home Assistant instance?

Check out the [Jonathan's Home Assistant Add-Ons][repository] repository for additional add-ons.

## License

MIT License

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/m/bradsjm/hassio-addons.svg
[commits]: https://github.com/bradsjm/hassio-addons/commits/main
[issue]: https://github.com/bradsjm/hassio-addons/issues
[license-shield]: https://img.shields.io/github/license/bradsjm/hassio-addons.svg
[releases-shield]: https://img.shields.io/github/release/bradsjm/hassio-addons/all.svg
[releases]: https://github.com/bradsjm/hassio-addons/releases
[repository]: https://github.com/bradsjm/hassio-addons
