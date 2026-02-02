---
name: ha-dashboards-cards
description: Research and implement Home Assistant dashboards and cards. Use when the user asks about Lovelace structure, views/sections, card types, resources, or HACS cards, and when mapping those needs to Home Assistant tools.
---

# Home Assistant Dashboards & Cards

## Purpose

Use this skill to find authoritative details for Lovelace dashboards and cards, then map those details to tool-driven updates (ha-mcp dashboard tools) or provide precise YAML/JSON examples.

## When to activate

- User asks about dashboard structure, views/sections, cards, or resources.
- User wants a new dashboard or modifications to an existing dashboard.
- User needs help with HACS cards or custom resources.

## Workflow

1. Determine whether to create a new dashboard or edit an existing one.
2. If editing, locate the card(s) first and then transform the config.
3. Prefer built-in cards unless the user asks for HACS/custom cards.
4. Provide minimal, correct config and cite references.
5. For uncertain card options, use card documentation tooling instead of guessing.

## Tooling map (ha-mcp)

- Discover entities: `ha_get_overview`, `ha_search_entities`
- Dashboard list/get: `ha_config_get_dashboard`
- Find cards: `ha_dashboard_find_card`
- Card schema discovery: `ha_get_card_types`, `ha_get_card_documentation`
- Update dashboard config: `ha_config_set_dashboard`
- Update dashboard metadata: `ha_config_update_dashboard_metadata`
- List/set/delete resources: `ha_config_list_dashboard_resources`, `ha_config_set_dashboard_resource`, `ha_config_set_inline_dashboard_resource`, `ha_config_delete_dashboard_resource`
- HACS cards: `ha_hacs_info`, `ha_hacs_list_installed`, `ha_hacs_search`, `ha_hacs_download`

## Output guidelines

- Provide a minimal dashboard/card snippet that compiles.
- Include a short rationale and cite the relevant docs.
- If entity IDs are needed, use discovery tools first.

## Caveats to always check

- URL paths for dashboards must contain a hyphen.
- Strategy dashboards require “Take Control” before editing.
- After resource changes, users may need a hard refresh.
- Use `ha_dashboard_find_card` to avoid index drift.
- Jinja templates are not evaluated in Lovelace YAML.
- Prefer template entities or conditional cards for dynamic UI needs.

## Examples

### Example: Create a dashboard with a single view

```yaml
views:
  - title: Home
    type: sections
    sections:
      - title: Climate
        cards:
          - type: tile
            entity: climate.living_room
            features:
              - type: target-temperature
```

### Example: Add a card via python_transform

```python
config["views"][0]["sections"][0]["cards"].append({"type": "tile", "entity": "light.kitchen"})
```

### Example: Update a card icon via jq_transform

```jq
.views[0].sections[0].cards[0].icon = "mdi:thermometer"
```

### Example: Register a custom resource

```yaml
url: /hacsfiles/lovelace-mushroom/mushroom.js
resource_type: module
```

### Example: Conditional card (swap UI by state)

```yaml
type: conditional
conditions:
  - entity: binary_sensor.garage_door
    state: "on"
card:
  type: tile
  entity: cover.garage_door
```

### Example: Visibility rules

```yaml
visibility:
  - condition: state
    entity: person.alex
    state: "home"
```

### Example: Minimal grid inside a section

```yaml
type: grid
columns: 2
cards:
  - type: tile
    entity: light.kitchen
  - type: tile
    entity: light.living_room
```

## Troubleshooting patterns

- **Card fails to render**: Confirm entity IDs and card type; check resource registration for custom cards.
- **Resource not loading**: Verify URL and type; hard refresh browser cache.
- **Edits not applied**: Confirm config_hash; re-fetch dashboard config and retry.
- **Indices shifted**: Use `ha_dashboard_find_card` to get a fresh path before a second edit.
- **Strategy dashboard**: Use “Take Control” before attempting edits via tools.
- **Dynamic template not working**: Remind that Jinja is not evaluated in core Lovelace; use template entities or conditional cards instead.

## References

- Design patterns: `references/DESIGN_PATTERNS.md`
- Card schema guide: `references/CARD_SCHEMA_GUIDE.md`
- Custom resources: `references/CUSTOM_RESOURCES.md`

# Home Assistant Dashboards & Cards Reference

## Primary documentation

- Dashboards overview: https://www.home-assistant.io/dashboards/
- Sections view: https://www.home-assistant.io/dashboards/sections/
- Views: https://www.home-assistant.io/dashboards/views/
- Cards overview: https://www.home-assistant.io/dashboards/cards/
- Tile card: https://www.home-assistant.io/dashboards/tile/
- Heading card: https://www.home-assistant.io/dashboards/heading/
- Grid card: https://www.home-assistant.io/dashboards/grid/
- Conditional card: https://www.home-assistant.io/dashboards/conditional/
- Card actions: https://www.home-assistant.io/dashboards/actions/
- Features: https://www.home-assistant.io/dashboards/features/
- Visibility rules: https://www.home-assistant.io/dashboards/visibility/
- Lovelace YAML mode: https://www.home-assistant.io/lovelace/yaml-mode/
- Lovelace UI editor: https://www.home-assistant.io/lovelace/editor/
- Lovelace resources: https://www.home-assistant.io/lovelace/dashboards-and-views/#resources

## Repo anchors (home-assistant/home-assistant.io)

- source/_docs/creating_themes.markdown
- source/_docs/lovelace.markdown
- source/_docs/lovelace/yaml-mode.markdown
- source/_docs/lovelace/editor.markdown
- source/_includes/lovelace/

## Key behavioral notes (short list)

- Dashboard URL paths must contain a hyphen.
- Strategy dashboards cannot be edited until “Take Control.”
- Custom card resources require a hard refresh after updates.
- Jinja templates are not evaluated in core Lovelace YAML.
- When unsure about a card option, use `ha_get_card_documentation()`.

## Example (official docs)

Tile card example from the official Tile card docs:

```yaml
type: tile
entity: cover.kitchen_window
```
