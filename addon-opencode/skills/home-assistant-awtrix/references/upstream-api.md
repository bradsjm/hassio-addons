# AWTRIX 3 upstream API references

Use upstream docs as the source of truth for MQTT payload formats and topic names.

## MQTT API (Custom Apps, Notifications, Settings)

- Upstream docs: https://github.com/Blueforcer/awtrix3/blob/main/docs/api.md
  - Topics include:
    - `<prefix>/custom/<appname>`
    - `<prefix>/notify`
    - `<prefix>/settings`

## HTTP API / filesystem

AWTRIX firmware variants expose a simple web server with filesystem endpoints; behavior can vary by build/device.

In this repo we keep an “observed endpoints” reference:
- `references/AWTRIX_HTTP_FILESYSTEM.md`

Treat the HTTP filesystem document as empirical/firmware-specific unless upstream documents the exact endpoints.
