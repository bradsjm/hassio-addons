# Changelog

## 0.2.0

- Pin Lunar MCPX to commit `e4a70047221fa015973d78858b7bdfd7ca321b32`.
- Store MCPX configuration in the Home Assistant add-on configuration mapping and mutable state in `/data`.
- Enable stdio MCP servers and add optional direct host Docker API support.
- Secure browser REST and Socket.IO authentication, CORS, and IP allowlisting; manage `auth.header: x-lunar-api-key` at startup.
- Migrate MCPX builds to Home Assistant's BuildKit actions and Docker Hub multi-architecture images.
