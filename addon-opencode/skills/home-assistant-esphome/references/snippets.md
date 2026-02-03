# ESPHome YAML snippets (starter patterns)

## Minimal, typical node

```yaml
esphome:
  name: ${node_name}
  friendly_name: ${friendly_name}

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

logger:

api:
  encryption:
    key: !secret esphome_api_key

ota:
```

## Naming guidance (avoid duplicates)

- Home Assistant generally prefixes entities with the device/node context; avoid repeating `${friendly_name}` inside each entity’s `name:` unless you have a specific reason.
- Prefer consistent `substitutions:` for `node_name` and `friendly_name` and keep per-entity `name:` short.

## “Invalid encryption key” quick checks

- Confirm the ESPHome node’s `api.encryption.key` matches what HA is asking for.
- In the HA ESPHome config flow this may be labeled `noise_psk` (same underlying 32-byte base64 key).
- If you regenerated keys, ensure the device is flashed with the new YAML (OTA/USB) before retrying HA config flow.
- If you adopted/renamed a device, make sure you’re not mixing “old node” vs “new node” configs.
