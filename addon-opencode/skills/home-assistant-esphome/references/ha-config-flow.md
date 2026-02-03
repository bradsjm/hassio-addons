# ESPHome integration config flow fields (HA core reference)

This file exists to prevent guessing what Home Assistant’s ESPHome integration stores/asks for during setup.

## Source-of-truth

Home Assistant Core:
- ESPHome config flow: `homeassistant/components/esphome/config_flow.py`
- Constants: `homeassistant/components/esphome/const.py`

## Encryption key field name: `noise_psk`

Home Assistant stores and prompts for the ESPHome native API encryption key under:
- `noise_psk` (constant `CONF_NOISE_PSK`)

This is the key used by the ESPHome native API encryption and is typically a base64-encoded key in ESPHome YAML (`api.encryption.key`).

## Official docs (starting points)

- HA ESPHome integration: https://www.home-assistant.io/integrations/esphome
- ESPHome API encryption: https://esphome.io/components/api.html
