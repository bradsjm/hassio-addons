---
name: ha-integrations-addons
description: Research and implement Home Assistant integrations, add-ons, updates, and system operations. Use when the user asks about config entries, add-ons, updates, restarts, or system health, and when mapping those needs to Home Assistant tools.
---

# Home Assistant Integrations & Add-ons

## Purpose

Use this skill to find authoritative details for integrations and add-ons, then map to tool-driven actions for discovery, enable/disable, updates, and safe operations.

## When to activate

- User asks about installed integrations, add-ons, updates, or system health.
- User wants to enable/disable or remove a config entry.
- User needs guidance on restart/reload flows.

## Workflow

1. Discover current integrations/add-ons and update availability.
2. Avoid destructive operations unless explicitly requested.
3. Prefer reloads over restarts when possible.
4. Provide minimal examples and cite references.

## Tooling map (ha-mcp)

- Integrations: `ha_get_integration`, `ha_set_integration_enabled`, `ha_delete_config_entry`
- Add-ons: `ha_get_addon`
- Updates: `ha_get_updates`
- Health: `ha_get_system_health`
- Reloads/restart: `ha_reload_core`, `ha_check_config`, `ha_restart`

## Output guidelines

- Summarize current state before changes.
- Call out risk and need for confirmation on destructive steps.

## Caveats to always check

- Deleting config entries is destructive and may remove devices/entities.
- Restart takes services offline briefly; prefer reloads when possible.
- Add-ons are only available on HA OS/Supervised.

## Examples

### Example: Enable a config entry

```yaml
entry_id: abc123
enabled: true
```

### Example: Reload automations

```yaml
target: automations
```

### Example: Check configuration before restart

```yaml
result: valid
```

### Example: List installed add-ons (conceptual)

```yaml
source: installed
include_stats: true
```

### Example: Disable a config entry

```yaml
entry_id: abc123
enabled: false
```

## Troubleshooting patterns

- **Integration not loaded**: check entry state via `ha_get_integration`.
- **Add-on missing**: verify install type and add-on store availability.
- **Update confusion**: use `ha_get_updates` to list categories and details.
- **Restart needed**: run `ha_check_config` before `ha_restart`.
- **Stuck setup**: disable/enable the integration to retry setup when safe.

## References

- Safe operations: `references/SAFE_OPERATIONS.md`
- Update flow: `references/UPDATE_FLOW.md`
- Add-on notes: `references/ADDON_NOTES.md`

# Home Assistant Integrations & Add-ons Reference

## Primary documentation

- Integrations: https://www.home-assistant.io/integrations/
- Add-ons: https://www.home-assistant.io/addons/
- Core updates: https://www.home-assistant.io/docs/installation/updates/
- System health: https://www.home-assistant.io/docs/configuration/troubleshooting/
- Reloading and restarting: https://www.home-assistant.io/docs/configuration/server-controls/

## Repo anchors (home-assistant/home-assistant.io)

- source/_docs/installation/updates.markdown
- source/_docs/configuration/troubleshooting.markdown
- source/_docs/configuration/server-controls.markdown
- source/_docs/addons/index.markdown

## Key behavioral notes (short list)

- Add-ons require HA OS or Supervised.
- Prefer reloads over restarts when supported.

## Example (official docs)

Add-on installation path from the official Add-ons docs:

```text
Settings > Add-ons > Add-on store
```
