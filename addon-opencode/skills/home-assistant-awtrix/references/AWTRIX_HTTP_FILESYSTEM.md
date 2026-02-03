# AWTRIX HTTP filesystem & utility endpoints (AWTRIX 3)

This reference captures the AWTRIX web UI behaviors and HTTP endpoints observed in this environment.

## Filesystem basics

### Common root layout
- `/ICONS` (icons)
- `/MELODIES`
- `/PALETTES`
- `/CUSTOMAPPS`
- `/DoNotTouch.json` (UI settings)

Some builds treat paths as case-sensitive (e.g., `/ICONS` works while `/icons` can return `BAD PATH`).

### List directory contents
- `GET http://<ip>/list?dir=/`
- `GET http://<ip>/list?dir=/ICONS`

Returns JSON array of objects like:
`{"type":"file|dir","size":"<bytes>","name":"<name>"}`.

### Get filesystem usage
- `GET http://<ip>/status`

Returns JSON including:
- `totalBytes` and `usedBytes`
- `mode`, `ssid`, and an `ip` field (32-bit integer formatted as `(ip & 255).(ip>>8 & 255).(ip>>16 & 255).(ip>>>24)` in the UI)

## `/edit` filesystem API

The built-in web file manager and other UI tools use `/edit` for CRUD operations.
The /edit endpoint uses the multipart filename parameter to specify the destination path, which is a common pattern in embedded web servers for file management operations.


### Upload/overwrite a file
- `POST http://<ip>/edit`
- Multipart field name to use: `data`
- Destination path comes from the multipart **filename**

Example:
```sh
curl -X POST -F 'data=@./local.gif;filename=/ICONS/1234.gif' http://<ip>/edit
```

### Create empty file/path
- `PUT http://<ip>/edit`
- Multipart fields: `path=/SOME/PATH`

### Rename/move a file
- `PUT http://<ip>/edit`
- Multipart fields: `path=/OLD/PATH`, `src=/NEW/PATH`

### Delete a file
- `DELETE http://<ip>/edit`
- Multipart fields: `path=/DIR/FILENAME`

## Other device web endpoints

### Version/info
- `GET /version` → version string (example observed: `0.98`)
- `GET /status` → filesystem + connection info

### Wi‑Fi management (used by main UI)
- `GET /scan` → JSON list of nearby SSIDs (can take several seconds)
- `POST /connect` → multipart fields: `ssid`, `password`, `persistent` (boolean); response text used as “new IP”
- `GET /restart` → restarts device
- `GET /save` → called after writing settings (appears to persist to flash)

### LiveView (used by `/screen`)
- `GET /api/screen` → current 8×32 pixel buffer as JSON
- `POST /api/nextapp` → next app in loop
- `POST /api/previousapp` → previous app in loop

### Backup/restore (used by `/backup`)
- Enumerate recursively with `GET /list?dir=<dir>`
- Download files by fetching their paths directly (e.g., `GET /ICONS/72.gif`)
- Restore uploads: the backup page uses `POST /edit?filename=<path>` (page-specific style)
- Reboot after restore: `POST /api/reboot`

## LaMetric icon import by ID (UI pattern)

Some UI builds include an icon tool that fetches LaMetric icon thumbnails:
- `GET https://developer.lametric.com/content/apps/icon_thumbs/<ID>`

Common behavior:
- `image/gif` → save as `/ICONS/<ID>.gif` (no conversion)
- `image/png` or `image/jpeg` → convert to JPEG and save as `/ICONS/<ID>.jpg` (PNG transparency is lost; canvas conversion typically composites to black)

The bundled script `scripts/awtrix_fs.py` implements this import workflow.

### Conversion dependency
For PNG/JPEG → JPG conversion, `scripts/awtrix_fs.py` uses Pillow. If Pillow is not available system-wide, the script creates a local virtual environment at `~/.codex/skills/home-assistant-awtrix/.venv` and installs Pillow there.

### HTTP Streaming Efficiency: The piped curl approach (downloading from source and piping directly to upload on target) is highly efficient for small files like these icons. This method:
- Avoids intermediate disk I/O
- Reduces memory usage
- Processes files in a streaming fashion (source → RAM → target)
