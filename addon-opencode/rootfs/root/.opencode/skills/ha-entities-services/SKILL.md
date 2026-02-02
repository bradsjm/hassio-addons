---
name: ha-entities-services
description: Research and implement Home Assistant entity discovery, states, helpers, and services. Use when the user asks about entities, states, helpers, labels, groups, or services, and when mapping those needs to Home Assistant tools.
---

# Home Assistant Entities & Services

## Purpose

Use this skill to find authoritative details for entities, helpers, services, and state modeling, then map to tool-driven discovery or changes in Home Assistant.

## When to activate

- User asks about entity IDs, state/attribute behavior, helpers, labels, or services.
- User wants to rename, move, hide, or label entities.
- User needs to call or discover services.

## Workflow

1. Discover entities and services first; do not guess IDs.
2. Prefer built-in helpers over templates for simple logic.
3. When changing entity metadata, confirm impact on automations.
4. Provide minimal examples and cite references.

## Tooling map (ha-mcp)

- Discover entities: `ha_get_overview`, `ha_search_entities`, `ha_get_state`
- Debug usage and history: `ha_deep_search`, `ha_get_history`, `ha_get_statistics`
- Manage entities: `ha_get_entity`, `ha_set_entity`, `ha_rename_entity`
- Devices: `ha_get_device`, `ha_update_device`
- Helpers: `ha_config_list_helpers`, `ha_config_set_helper`, `ha_create_config_entry_helper`
- Labels: `ha_config_get_label`, `ha_config_set_label`, `ha_manage_entity_labels`
- Groups: `ha_config_list_groups`, `ha_config_set_group`
- Services: `ha_list_services`, `ha_call_service`

## Output guidelines

- Provide a minimal example or tool call map.
- Cite relevant docs.
- Ask only for missing details after discovery.

## Templating and limited templates

Templates used in some triggers and `trigger_variables` are **limited templates** and do not support many Home Assistant template extensions (for example `states` object access, attribute helpers, `expand`, and time helpers like `now()`). If a template fails only in a trigger field, move logic into conditions or a template entity.

## Caveats to always check

- Renaming an entity does not update automations/scripts/dashboards.
- Device rename does not rename entities.
- Some entities cannot be renamed (no unique_id).

## Examples

### Example: Call a service

```yaml
service: light.turn_on
target:
  entity_id: light.living_room
data:
  brightness: 150
```

### Example: Create a helper (input_boolean)

```yaml
name: Quiet Mode
icon: mdi:volume-off
```

### Example: Rename an entity

```yaml
entity_id: sensor.old_name
new_entity_id: sensor.living_room_temperature
name: Living Room Temperature
```

### Example: Add labels to entities

```yaml
entity_id:
  - light.kitchen
  - light.living_room
operation: add
labels:
  - evening
```

### Example: Create a group

```yaml
object_id: living_room_lights
name: Living Room Lights
entities:
  - light.living_room_main
  - light.living_room_lamp
```

## Troubleshooting patterns

- **Service fails**: confirm service exists and required fields via `ha_list_services`.
- **Entity not found**: use `ha_search_entities` with domain filter.
- **Unexpected state**: check `ha_get_state` and the entity attributes.
- **Rename side effects**: remind that automations/scripts/dashboards won't update automatically.
- **Helper missing**: verify whether it was created in YAML vs UI; tool lists only storage-based helpers.
- **Where is this referenced?**: use `ha_deep_search` to locate automations/scripts using the entity.
- **State history confusion**: use `ha_get_history` for recent changes and `ha_get_statistics` for long-term trends.
- **Template errors**: validate whether the template context is limited; prefer template entities for complex logic.

## References

- Limited template quick ref: `references/LIMITED_TEMPLATES.md`
- State object quick ref: `references/STATE_OBJECT_QUICKREF.md`
- Entity rename impact: `references/ENTITY_RENAME_IMPACT.md`
- Helpers vs templates: `references/HELPERS_VS_TEMPLATES.md`

# Home Assistant Entities & Services Reference

## Primary documentation

- Entity model: https://www.home-assistant.io/docs/configuration/state_object/
- Entity registry: https://www.home-assistant.io/docs/configuration/entity-registry/
- Services: https://www.home-assistant.io/docs/scripts/service-calls/
- Helpers: https://www.home-assistant.io/docs/tools/helpers/
- Templating (Jinja + limited templates): https://www.home-assistant.io/docs/configuration/templating/
- Template integration: https://www.home-assistant.io/integrations/template
- Labels: https://www.home-assistant.io/docs/organizing/labels/
- Groups: https://www.home-assistant.io/docs/organizing/groups/
- Devices and areas: https://www.home-assistant.io/docs/organizing/

## Repo anchors (home-assistant/home-assistant.io)

- source/_docs/configuration/state_object.markdown
- source/_docs/configuration/entity-registry.markdown
- source/_docs/scripts/service-calls.markdown
- source/_docs/tools/helpers.markdown
- source/_docs/organizing/labels.markdown
- source/_docs/organizing/groups.markdown
- source/_docs/organizing/index.markdown

## Key behavioral notes (short list)

- Entity renames do not update automations/scripts/dashboards.
- Device renames do not rename entities.

## Example (official docs)

State object example from the State and state object docs:

```jinja2
{{ states.switch.my_switch.last_changed }}
```
