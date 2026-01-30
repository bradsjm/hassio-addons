# Home Assistant Add-on: OpenCode

## How to use

This add-on runs the OpenCode web or server mode inside Home Assistant.

### Options

- `mode`: `web` or `serve` (web UI or headless server)
- `port`: Port to listen on (default `4096`)
- `hostname`: Bind address (default `0.0.0.0`)
- `mdns`: Enable mDNS discovery (default `false`)
- `cors`: Comma-separated list of CORS origins
- `username`: HTTP basic auth username (default `opencode`)
- `password`: HTTP basic auth password (optional)

Authentication is enabled when `password` is set. The web UI and API are
available at `http://[HOST]:[PORT:4096]`.
