# AWTRIX 3 in Home Assistant (MQTT-based) — Control & App Creation

This document focuses on controlling AWTRIX 3 devices **from Home Assistant**, and creating/updating **Custom Apps** and **Notifications** using Home Assistant’s `mqtt.publish` service.

Note: This file includes an example device from one Home Assistant instance. Do not assume the entity IDs exist in another system; always discover the device topic sensor first.

## Discovery (do this first)

- Find the AWTRIX “device topic” sensor(s): `ha_search_entities(query="awtrix device topic", domain_filter="sensor")`
- If you only know the room/name: `ha_search_entities(query="awtrix", limit=50)`

Example device in this HA instance:
- Device: **AWTRIX Master Bedroom Display** (MQTT-discovered)
- MQTT topic prefix (device “topic”): `sensor.awtrix_master_bedroom_display_device_topic` → `awtrix_masterbedroom`

---

## 1) How AWTRIX shows up in Home Assistant

AWTRIX exposes a set of MQTT-discovered entities that map to common controls/sensors. For the example device:

### Core controls (entities)
- Main “matrix light”: `light.master_bedroom_awtrix` (RGB; often used for moodlight/overall matrix state)
- Transition enable: `switch.awtrix_master_bedroom_display_transition`
- Transition effect: `select.awtrix_master_bedroom_display_transition_effect`
- Brightness mode: `select.awtrix_master_bedroom_display_brightness_mode`
- Loop navigation: `button.awtrix_master_bedroom_display_next_app`, `button.awtrix_master_bedroom_display_previous_app`
- Dismiss held notification: `button.awtrix_master_bedroom_display_dismiss_notification`
- Start update: `button.awtrix_master_bedroom_display_start_update`
- Indicators (as lights): `light.awtrix_master_bedroom_display_indicator_1`, `light.awtrix_master_bedroom_display_indicator_2`, `light.awtrix_master_bedroom_display_indicator_3`

### Common sensors (entities)
- Device topic/prefix: `sensor.awtrix_master_bedroom_display_device_topic` (example value: `awtrix_masterbedroom`)
- Network: `sensor.awtrix_master_bedroom_display_ip_address`, `sensor.awtrix_master_bedroom_display_wifi_strength`
- Environment: `sensor.awtrix_master_bedroom_display_temperature`, `sensor.awtrix_master_bedroom_display_humidity`, `sensor.awtrix_master_bedroom_display_illuminance`
- Health: `sensor.awtrix_master_bedroom_display_battery`, `sensor.awtrix_master_bedroom_display_uptime`, `sensor.awtrix_master_bedroom_display_free_ram`, `sensor.awtrix_master_bedroom_display_version`

### Button input (entities)
- `binary_sensor.awtrix_master_bedroom_display_button_left`
- `binary_sensor.awtrix_master_bedroom_display_button_select`
- `binary_sensor.awtrix_master_bedroom_display_button_right`

Use these built-in entities where possible. For custom pages/apps, use MQTT publish (below).

---

## 2) Finding the right MQTT prefix (topic root) in HA

Each AWTRIX device exposes its topic/prefix as a sensor:
- Example: `sensor.awtrix_master_bedroom_display_device_topic` → `awtrix_masterbedroom`

In automations/scripts, template the prefix:
```yaml
{% set awtrix = states('sensor.awtrix_master_bedroom_display_device_topic') %}
```

Then build topics like:
- `{{ awtrix }}/custom/<appname>`
- `{{ awtrix }}/notify`
- `{{ awtrix }}/settings`

---

## 3) Creating & updating AWTRIX Custom Apps from Home Assistant

AWTRIX “Custom Apps” are loop pages created by publishing JSON to:
- MQTT topic: `PREFIX/custom/<appname>`

In Home Assistant, do this with `mqtt.publish`.

### Minimal example: create/update a custom app
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/custom/hello"
  payload: >-
    {{ {"text":"Hello from Home Assistant","duration":10} | tojson }}
  retain: false
  qos: 0
```

### Example: custom app with icon + background effect
Notes:
- `icon` is an icon ID or filename already present on the device.
- `effect` is a named effect available on the device (device publishes available effects via `PREFIX/stats/effects`).
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/custom/weather"
  payload: >-
    {{ {
      "text":"72°F  •  Clear",
      "icon":"5029",
      "effect":"ColorWaves",
      "duration":15,
      "repeat":1
    } | tojson }}
```

### Delete a custom app (remove it from the loop)
Publish an **empty payload** to the same topic. In HA, omit `payload`:
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/custom/weather"
```

### Multiple custom apps in one publish (suffixing)
Publishing an array creates multiple apps internally (`name0`, `name1`, …):
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/custom/quick"
  payload: >-
    {{ [
      {"text":"Page 1","duration":5},
      {"text":"Page 2","duration":5}
    ] | tojson }}
```
To delete all `quick*` apps, publish empty payload to `/custom/quick`.

---

## 4) Sending Notifications from Home Assistant

Notifications are sent by publishing JSON to:
- MQTT topic: `PREFIX/notify`

### Example: simple notification
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/notify"
  payload: >-
    {{ {"text":"Front door opened","duration":8} | tojson }}
```

### Example: held notification that must be dismissed
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/notify"
  payload: >-
    {{ {
      "text":"Alarm armed",
      "hold": true,
      "wakeup": true,
      "duration":30
    } | tojson }}
```

Dismiss it using the built-in HA button entity:
- `button.awtrix_master_bedroom_display_dismiss_notification`

Or publish empty payload to:
- `PREFIX/notify/dismiss`

---

## 5) Loop control from Home Assistant (switching apps)

Prefer the discovered buttons:
- Next: `button.awtrix_master_bedroom_display_next_app`
- Previous: `button.awtrix_master_bedroom_display_previous_app`

MQTT alternative (empty payload):
- `PREFIX/nextapp`
- `PREFIX/previousapp`

Switch to a specific app name (JSON):
- Topic: `PREFIX/switch`
- Payload: `{"name":"Time"}` (built-ins include `Time`, `Date`, `Temperature`, `Humidity`, `Battery`)

---

## 6) Indicators from Home Assistant

Prefer the discovered indicator lights:
- `light.awtrix_master_bedroom_display_indicator_1`
- `light.awtrix_master_bedroom_display_indicator_2`
- `light.awtrix_master_bedroom_display_indicator_3`

These map to AWTRIX “colored indicators” and support RGB color.

MQTT alternative:
- `PREFIX/indicator1|2|3` with payload like `{"color":[255,0,0]}` or `{"color":"#FF0000"}`.

---

## 7) Settings from Home Assistant

For common settings, prefer the discovered entities:
- Transition toggle: `switch.awtrix_master_bedroom_display_transition`
- Transition effect: `select.awtrix_master_bedroom_display_transition_effect`
- Brightness mode: `select.awtrix_master_bedroom_display_brightness_mode`

For additional global settings (advanced), publish JSON to:
- MQTT topic: `PREFIX/settings`

Example: set time/date formatting and scroll speed modifier:
```yaml
action: mqtt.publish
data:
  topic: "{{ states('sensor.awtrix_master_bedroom_display_device_topic') }}/settings"
  payload: >-
    {{ {
      "TFORMAT":"%H:%M",
      "DFORMAT":"%m/%d",
      "SSPEED": 100
    } | tojson }}
```

---

## 8) Noisy `current_app` sensor: disable by default

Some AWTRIX devices expose a `sensor.*_current_app` that changes constantly as the device cycles apps. This can:
- Spam the state machine/history
- Trigger unintended automations
- Increase recorder churn

Recommendation:
- Disable `*_current_app` unless you explicitly need it for an automation.

How:
1) UI: **Settings → Devices & services → Entities**, find the `Current app` entity, click it, and **Disable**.
2) Service: `homeassistant.disable_entity` with the entity id.

If you need it for a specific automation:
- Enable it temporarily, or
- Keep it enabled but exclude it from recorder/history and use careful conditions (e.g., time windows, debounce, or ignore loop transitions).

---

## 9) Practical Home Assistant patterns

### A) Create a reusable script per AWTRIX device
Make a script like `script.awtrix_master_bedroom_notify` that accepts fields (`text`, `icon`, `duration`) and does `mqtt.publish` to `{{ prefix }}/notify`.

### B) Keep payloads small
AWTRIX can be constrained by receive buffer size; prefer short payloads and avoid giant `draw` arrays unless necessary.

### C) Prefer entity controls for “housekeeping”
Use HA’s existing entities (brightness mode, transition effect, dismiss, next/previous) instead of reimplementing those with raw MQTT topics.

---

## 10) Filesystem (ICON) management
There is a small amount of filesystem space for icons, melodies, palettes and custom apps.

### Directory layout (SPIFFS/LittleFS)
Common top-level directories (case-sensitive on some builds):
- `/ICONS`
- `/MELODIES`
- `/PALETTES`
- `/CUSTOMAPPS`

The root usually also contains `DoNotTouch.json` (used by the device UI for settings).

Note: Some builds treat paths as case-sensitive (e.g., `/ICONS` works but `/icons` returns `BAD PATH`).

### List files / folders
- `GET http://<ip>/list?dir=/` (or `dir=/ICONS`, etc.)
- Returns JSON like: `[{"type":"dir|file","name":"...","size":"..."}]`
- Missing `dir` typically returns `400 Bad Request`

### Filesystem size / usage
- `GET http://<ip>/status`
- Returns JSON including `totalBytes` and `usedBytes` (compute free space as `totalBytes - usedBytes`).
- The UI exposes `ip` as a 32-bit integer and formats it to dotted IPv4 as: `(ip & 255).(ip>>8 & 255).(ip>>16 & 255).(ip>>>24)`.

### Upload / overwrite a file
`POST http://<ip>/edit`

Two observed multipart upload patterns:
1) **Destination path from multipart filename** (common for raw file uploads):
   - Multipart field name: `data` (used by the built-in file editor UI)
   - The uploaded file’s multipart **filename** is the destination path (e.g., `/ICONS/72.gif`)
2) **Alternate field name**:
   - Multipart field name: `image` (used by some UI features like logo/icon import)

Example (upload local file as an icon):
```sh
curl -X POST -F 'data=@./72.gif;filename=/ICONS/72.gif' http://<ip>/edit
```

### Create empty file (or folder entry, depending on build)
`PUT http://<ip>/edit` with multipart form field:
- `path=/SOME/PATH`

### Rename / move a file
`PUT http://<ip>/edit` with multipart form fields:
- `path=/OLD/PATH`
- `src=/NEW/PATH`

This is the rename/move mechanism used by the web file manager.

### Delete a file
`DELETE http://<ip>/edit` with multipart form field:
- `path=/DIR/FILENAME`

---

## 11) Device Web UI endpoints (non-MQTT)
These endpoints are used by AWTRIX’s built-in web UI and can be helpful for debugging or device management.

### Info / status
- `GET /version` → version string (e.g., `0.98`)
- `GET /status` → filesystem stats + connection mode + network info

### Wi‑Fi setup helpers
- `GET /scan` → JSON list of nearby Wi‑Fi networks (can take several seconds)
- `POST /connect` → form fields: `ssid`, `password`, `persistent` (boolean); response text is used as “new IP” in the UI
- `GET /restart` → triggers device restart (used by the UI)
- `GET /save` → called after writing settings; appears to persist to flash

### LiveView (screen)
The LiveView page (`/screen`) uses these endpoints:
- `GET /api/screen` → returns the current 8×32 pixel buffer as JSON
- `POST /api/nextapp` → advance loop/app
- `POST /api/previousapp` → go back in loop/app

### Backup / restore
The Backup page (`/backup`) implements:
- Enumerate: `GET /list?dir=<dir>` recursively
- Download files by fetching their paths directly (e.g., `GET /ICONS/72.gif`)
- Restore uploads to: `POST /edit?filename=<path>` (page-specific upload style)
- Reboot after restore: `POST /api/reboot`

### Firmware / filesystem updates
The Update page (`/update`) is a simple HTML form that posts firmware/filesystem images to the device.

---

## 12) LaMetric icon preview + import (via Web UI)
Some AWTRIX UI builds include an “icon” tool that can preview/download icons from LaMetric’s icon CDN:

### Preview
- Image preview URL: `https://developer.lametric.com/content/apps/icon_thumbs/<ID>`

### Download + save to device
Observed behavior:
- Downloads the icon from the LaMetric URL and inspects `Content-Type`:
  - `image/gif` → saved as `/ICONS/<ID>.gif` (no conversion)
  - `image/png` or `image/jpeg` → converted to **JPEG** via a canvas and saved as `/ICONS/<ID>.jpg` (PNG transparency is lost)
- Uploads to the device using `POST /edit` with multipart field name `image` and filename `ICONS/<ID>.gif|.jpg` (some builds omit the leading `/`).

Notes:
- If uploads land in the wrong place, ensure the destination path includes a leading slash (`/ICONS/...`).
- Some implementations set `fetch(..., { mode: "no-cors" })` when posting to `/edit`; this can make the response “opaque” even though the upload succeeds.
