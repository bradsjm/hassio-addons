# Integration authoring checklist (native patterns)

## Before coding

- Identify the integration domain name (stable, snake_case).
- Decide if it is config-entry-based (recommended) vs YAML (avoid new YAML integrations).
- Identify authentication model and failure modes (offline, invalid auth, rate limits).

## During implementation

- Use `DataUpdateCoordinator` for shared I/O and throttling when polling (or when you need a central cache).
- Use `CoordinatorEntity` (or `coordinator.async_add_listener`) so entities update efficiently.
- Raise `ConfigEntryNotReady` for transient failures on setup to let HA retry.
- Raise `ConfigEntryAuthFailed` for invalid auth so HA prompts reauth.
- Keep I/O out of entity properties; entities should read cached coordinator data.
- Provide `device_info` so entities group under a device in the UI.

## Before shipping

- Add `services.yaml` for custom services (only if needed; prefer standard services first).
- Add translations (`strings.json` + `translations/*.json`) for config flow UX.
- Run through quality scale basics (docs, diagnostics if applicable, config flow, tests).
