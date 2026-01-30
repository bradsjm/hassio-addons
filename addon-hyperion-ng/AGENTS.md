# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

This is a Home Assistant add-on repository containing Docker-based add-ons for Home Assistant. Each add-on is packaged as a Docker container with specific configuration files:

- `repository.json` - Repository metadata defining the add-on collection
- `addon-*/config.json` - Add-on configuration including ports, permissions, and hardware access
- `addon-*/build.json` - Docker build configuration with base images and build arguments
- `addon-*/Dockerfile` - Container definition with dependencies and runtime setup
- `addon-*/run.sh` - Entry point script for the add-on service

### Hyperion.NG Add-on Structure

The main add-on (`addon-hyperion-ng`) provides ambient lighting functionality:
- Downloads and installs Hyperion.NG binaries based on architecture (amd64/armhf/aarch64)
- Requires extensive hardware permissions (USB, video, GPIO, SPI devices)
- Runs as privileged container with direct hardware access
- Configuration stored in `/config/hyperion` within the container

## Development

### Version Updates
When updating add-on versions:
1. Update version in `addon-*/config.json`
2. Ensure corresponding binary release exists at the download URL
3. Test across all supported architectures if possible

### Docker Build
Add-ons use Home Assistant base images:
- `homeassistant/amd64-base-debian` (amd64)
- `homeassistant/armhf-base-raspbian` (armhf) 
- `homeassistant/aarch64-base-debian` (aarch64)

### Hardware Access
The Hyperion.NG add-on requires specific device access patterns:
- Video devices (`/dev/fb0`, `/dev/amvideo`, `/dev/vchiq`)
- SPI interface (`/dev/spidev0.0`)
- Memory access (`/dev/mem`)
- USB and GPIO permissions