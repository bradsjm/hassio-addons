# AGENTS.md

This repository contains Home Assistant add-ons for Hyperion.NG, OpenCode, and OpenChamber.
Use this file as the primary guide for agentic coding work here.

## Repo Overview

- Add-on paths: `addon-hyperion-ng/`, `addon-opencode/`, `addon-openchamber/`
- Core metadata: `repository.json`
- Hyperion config: `addon-hyperion-ng/config.yaml`
- Hyperion container definition: `addon-hyperion-ng/Dockerfile`
- Hyperion runtime entrypoint: `addon-hyperion-ng/run.sh`
- OpenCode config: `addon-opencode/config.yaml`
- OpenCode build metadata: `addon-opencode/build.yaml`
- OpenCode container definition: `addon-opencode/Dockerfile`
- OpenCode runtime entrypoint: `addon-opencode/rootfs/etc/services.d/opencode/run`
- OpenChamber config: `addon-openchamber/config.yaml`
- OpenChamber build metadata: `addon-openchamber/build.yaml`
- OpenChamber container definition: `addon-openchamber/Dockerfile`
- OpenChamber runtime entrypoint: `addon-openchamber/rootfs/etc/services.d/openchamber/run`
- Helper scripts: `addon-hyperion-ng/download-hyperion.sh`, `.github/scripts/*`

## Build / Lint / Test Commands

There are no explicit lint or test frameworks in this repo.
Use the scripts below for validation and smoke testing.

### Build (local or CI-like)

- Build the Hyperion image for amd64:
  `docker buildx build --pull --platform linux/amd64 --build-arg BUILD_VERSION=2.2.1 --build-arg BUILD_ARCH=amd64 --load -t local/addon-hyperion-ng:2.2.1-amd64 addon-hyperion-ng`

- Validate the Hyperion aarch64 build:
  `docker buildx build --pull --platform linux/arm64 --build-arg BUILD_VERSION=2.2.1 --build-arg BUILD_ARCH=aarch64 --output type=cacheonly addon-hyperion-ng`

- Build OpenCode add-on image for a single architecture:
  `./.github/scripts/build-opencode.sh amd64`

- Build all OpenCode architectures:
  `./.github/scripts/build-opencode.sh all`

- Build OpenChamber add-on image for a single architecture:
  `./.github/scripts/build-openchamber.sh amd64`

- Build all OpenChamber architectures:
  `./.github/scripts/build-openchamber.sh all`

Notes:
- Hyperion CI uses the pinned `home-assistant/builder` composite actions to publish `docker.io/bradsjm/addon-hyperion-ng` as a multi-architecture manifest on pushes to `main`.

### Smoke Tests (single "test")

There is no formal test suite. Use the download script to validate release assets.

- Validate a single architecture download (acts like a single test):
  `./addon-hyperion-ng/download-hyperion.sh <version> <arch> /tmp/hyperion-test`

Examples:
- `mkdir -p /tmp/hyperion-test`
- `./addon-hyperion-ng/download-hyperion.sh 2.2.1 amd64 /tmp/hyperion-test`

### Version Update Helper

- Update add-on version from GitHub releases:
  `./.github/scripts/update-hyperion-version.sh`

This script reads and atomically updates the top-level version in `addon-hyperion-ng/config.yaml`.

## Code Style Guidelines

### General Principles

- Keep changes minimal and consistent with existing patterns.
- Prefer explicit, readable shell and Dockerfile steps over cleverness.
- Do not introduce new tooling without a clear need.

### YAML (config.yaml) and JSON (repository.json)

- Use 2-space indentation.
- Keep keys sorted only if the file already uses a stable order.
- Avoid trailing commas.
- Keep long strings on a single line unless the existing file uses wrapping.

### Shell Scripts (.sh)

- Use `#!/bin/bash` or `#!/usr/bin/with-contenv bashio` as already in use.
- Start with strict mode where appropriate: `set -euo pipefail`.
- Use functions for non-trivial steps (see `download-hyperion.sh`).
- Log errors to stderr and exit non-zero on failures.
- Prefer explicit variable names: `build_arch`, `output_dir`, `download_url`.
- Quote variables unless you intentionally rely on word splitting.

### Dockerfile

- Use the explicit pinned Home Assistant Debian base and the `BUILD_VERSION` and `BUILD_ARCH` build arguments.
- Keep package install steps consolidated and clean `apt` lists in the same layer.
- Preserve existing validation steps after installation.
- Do not remove verification of `hyperiond` installation.

### Naming Conventions

- Files and directories: kebab-case (`addon-hyperion-ng`).
- Shell functions: lower_snake_case.
- Shell variables: lower_snake_case; constants in upper case.
- JSON keys and add-on fields must follow Home Assistant add-on spec.

### Imports / Dependencies

- There are no language imports beyond shell and Docker.
- Prefer existing tools: `curl`, `jq`, `tar`, `gzip`.
- Do not add new dependencies to the base image without a strong reason.

### Error Handling

- Fail fast with clear error messages.
- Validate inputs and environment before work begins.
- When downloading, keep retry logic and size checks intact.
- For scripts invoked in CI, avoid interactive prompts unless explicitly in local mode.

### Configuration & Versions

- Update `addon-hyperion-ng/config.yaml` version when bumping Hyperion.
- Ensure the release assets exist for all supported architectures.
- Ensure the pinned Dockerfile base image supports both configured architectures.

## Project-Specific Conventions

- Add-on is hardware-privileged; do not remove required permissions or devices.
- Keep `run.sh` minimal and focused on launching `hyperiond`.
- Use `/config/hyperion` for persistent configuration.

## CI / GitHub Actions

- Workflows in `.github/workflows/`: `addon-hyperion-ng.yml`, `addon-opencode.yml`, `addon-openchamber.yml`
- Hyperion CI validates the configured release assets, builds each supported architecture, and publishes a generic manifest only from `main` pushes.
- CI uses helper scripts in `.github/scripts/`.

## Cursor / Copilot Rules

- No Cursor rules found in `.cursor/rules/` or `.cursorrules`.
- No Copilot instructions found in `.github/copilot-instructions.md`.

## Agent Workflow Tips

- Prefer reading and modifying existing files over adding new ones.
- If you add new scripts, make them executable and document usage here.
- Avoid large refactors; this repo is primarily configuration and scripts.
- Preserve ASCII-only content unless a file already uses Unicode.

## Single-File Edit Checklist

- Update only the target file unless dependencies require a change.
- Keep file formatting consistent with current style.
- Verify scripts with `bash -n` if you modify them.

## Multi-File Change Checklist

- Update `config.yaml` if version changes.
- Verify `download-hyperion.sh` still supports all architectures.
- Re-run the download smoke test for at least one arch.

## When Unsure

- Follow the patterns already established in `addon-hyperion-ng/`.
- Keep changes small and well-scoped.
