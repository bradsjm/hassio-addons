# Automation config schema (source-of-truth)

This reference exists to avoid guessing what fields Home Assistant accepts in an automation’s YAML/config.

## Source-of-truth

Home Assistant Core defines the automation config validation schema in:
- `homeassistant/components/automation/config.py` (`PLATFORM_SCHEMA`)

If there is any discrepancy between a blog/forum snippet and “what HA accepts”, trust the core schema.

## What the schema allows (high level)

Automations are validated using a schema built on `script.make_script_schema(...)` and include:

- Required:
  - `id`
  - `alias`
  - `triggers` (plural)
  - `actions` (plural)
- Optional:
  - `description`
  - `conditions`
  - `variables`
  - `trigger_variables`
  - `trace`
  - `initial_state`
  - `hide_entity` (deprecated)

Backward-compatible renames are supported:
- `trigger` → `triggers`
- `action` → `actions`
- `condition` → `conditions`

## Important: icon is not part of automation YAML

The automation schema does **not** include an `icon` field. If you need to change an automation’s icon, that is typically done via the UI (entity customization), not by changing the automation YAML/config via `ha_config_set_automation`.

## Practical rule when editing via HA MCP

- If you include unsupported keys in `ha_config_set_automation`, Home Assistant will reject the configuration (schema validation error).
- When unsure, consult the core schema and/or the official docs:
  - Automation YAML: https://www.home-assistant.io/docs/automation/yaml/
