---
name: ha-automation-scripts
description: Research and implement Home Assistant automations, scripts, and blueprints. Use when the user asks for automation/script syntax, triggers, conditions, actions, templating, run modes, or troubleshooting, and when mapping those needs to Home Assistant tools.
---

# Home Assistant Automations & Scripts

## Purpose

Use this skill to find authoritative technical details for Home Assistant automations, scripts, and blueprints, then map those details to tool-driven actions (ha-mcp tools) or provide precise YAML/JSON examples.

## When to activate

- User asks about automation or script syntax, triggers, conditions, actions, templating, run modes, or troubleshooting.
- User wants a blueprint explanation or a blueprint-based automation.
- User needs guidance to implement or inspect automations/scripts with Home Assistant tools.

## Workflow

1. Identify whether the request is instance-specific or general syntax.
2. For instance-specific requests, discover entities/services first (avoid guessing entity IDs).
3. Prefer native triggers/conditions/actions over templates where possible.
4. Draft minimal, correct YAML/JSON with clear rationale and cite references.
5. Call out caveats that commonly break automations.

## Tooling map (ha-mcp)

- Discover entities: `ha_get_overview`, `ha_search_entities`
- Discover services: `ha_list_services`
- Inspect existing automations/scripts: `ha_config_get_automation`, `ha_config_get_script`, `ha_deep_search`
- Create/update automation: `ha_config_set_automation`
- Create/update script: `ha_config_set_script`
- Validate templates: `ha_eval_template`
- Troubleshoot runs: `ha_get_automation_traces`, `ha_get_logbook`
- Debug history/trends: `ha_get_history`, `ha_get_statistics`
- Find references: `ha_deep_search`
- Blueprints: `ha_get_blueprint`, `ha_import_blueprint`

## Output guidelines

- Provide a minimal example (YAML or JSON) that compiles.
- Include a short rationale and cite the relevant docs.
- Mention caveats for any use of templates, `for`, or waits.
- If required inputs are unknown (e.g., entity IDs), ask for only the missing details after doing all possible discovery.

## Templating and limited templates

Templates used in some trigger fields and `trigger_variables` are **limited templates** and only support a subset of Home Assistant template extensions. Commonly unsupported in limited templates:

- `states` object iteration/access helpers and related shortcuts
- Attribute helpers and `state_attr`/`is_state_attr`
- Group expansion via `expand`
- `state_translated`
- `distance()` and `closest()`
- `device_attr()` / `is_device_attr()`
- `config_entry_attr()`
- Time helpers: `now()`, `utcnow()`, `time_since()`, `time_until()`, `today_at()`

Rule of thumb: if a template works in an action/condition but fails in a trigger field or `trigger_variables`, check the limited template restrictions.

## Examples

### Example: State trigger with `for`

Use when a device should remain in a state before acting. Mention the restart/reload reset caveat.

```yaml
automation:
  - alias: "Turn lights off after 10 minutes idle"
    trigger:
      - platform: state
        entity_id: binary_sensor.living_room_motion
        to: "off"
        for: "00:10:00"
    action:
      - action: light.turn_off
        target:
          area_id: living_room
```

### Example: Template guard with native trigger

Prefer native triggers, then use a template condition only when required.

```yaml
automation:
  - alias: "Notify if humidity is high"
    trigger:
      - platform: numeric_state
        entity_id: sensor.bathroom_humidity
        above: 70
    condition:
      - condition: template
        value_template: "{{ states('sensor.outdoor_temp') | float(0) < 10 }}"
    action:
      - action: notify.notify
        data:
          message: "Bathroom humidity is high and it's cold outside."
```

### Example: Blueprint-based automation

Use when a blueprint is requested; link to schema/selectors and require `min_version` if using newer features.

```yaml
automation:
  - alias: "Motion Light Kitchen"
    use_blueprint:
      path: homeassistant/motion_light.yaml
      input:
        motion_entity: binary_sensor.kitchen_motion
        light_target:
          entity_id: light.kitchen
        no_motion_wait: 120
```

### Example: Script with wait and timeout

Call out `wait` variables and `continue_on_timeout` behavior.

```yaml
script:
  door_wait:
    sequence:
      - wait_template: "{{ is_state('binary_sensor.door', 'on') }}"
        timeout: "00:01:00"
        continue_on_timeout: false
      - action: notify.notify
        data:
          message: "Door opened."
```

### Example: Trigger variables (limited templates)

Use only limited-template-safe values in `trigger_variables`.

```yaml
automation:
  trigger_variables:
    my_event: example_event
  trigger:
    - platform: event
      event_type: "{{ my_event }}"
  action:
    - action: notify.notify
      data:
        message: "Received {{ trigger.event.event_type }}"
```

## Troubleshooting patterns

- **Automation not triggering**: Check trigger config and recent traces (`ha_get_automation_traces`). Verify entity IDs with `ha_search_entities`.
- **Trigger fires but actions do nothing**: Ensure conditions passed, target entities exist, and the service is valid (`ha_list_services`).
- **Template seems stale**: Confirm limited-template fields aren’t expected to update dynamically; use native triggers or re-evaluate via `ha_eval_template`.
- **`for` timing issues**: Remember `for` resets on restart/reload; use `input_datetime` if persistence is needed.
- **Waits never complete**: `wait_template` only re-evaluates on referenced entity changes; include a time/date entity if needed.
- **Device trigger confusion**: Create in UI and copy YAML; device triggers are integration-defined.
- **Unexpected state changes**: Use `ha_get_history` for raw state changes and `ha_get_logbook` for event timeline.
- **Long-term trends**: Use `ha_get_statistics` for daily/weekly rollups.
- **Where is this used?**: Use `ha_deep_search` to find automations/scripts referencing an entity or service.
- **Trigger template fails**: Validate whether the template context is limited; move logic to conditions or template entities if needed.

## Caveats to always check

- `trigger_variables` and limited-template fields are evaluated only at setup time.
- `for` timers reset on Home Assistant restart or automation reload.
- `wait_template` only re-evaluates on referenced entity changes (use a time/date entity if needed).
- Parallel actions have no order guarantee and can cause variable collisions.
- Device triggers are integration-defined; prefer creating in UI and copy YAML if unsure.

## References

- Limited template quick ref: `references/LIMITED_TEMPLATES.md`
- Debug workflows: `references/DEBUG_WORKFLOWS.md`
- Template entities: `references/TEMPLATE_ENTITY_GUIDE.md`

## Primary documentation

- Automations overview: https://www.home-assistant.io/docs/automation/
- Automation triggers: https://www.home-assistant.io/docs/automation/trigger/
- Automation conditions: https://www.home-assistant.io/docs/automation/condition/
- Automation actions: https://www.home-assistant.io/docs/automation/action/
- Automation templating: https://www.home-assistant.io/docs/automation/templating/
- Templating (Jinja + limited templates): https://www.home-assistant.io/docs/configuration/templating/
- State object model: https://www.home-assistant.io/docs/configuration/state_object/
- Automation run modes: https://www.home-assistant.io/docs/automation/modes/
- Automation actions (services): https://www.home-assistant.io/docs/automation/services/
- Troubleshooting automations: https://www.home-assistant.io/docs/automation/troubleshooting/
- Automation YAML: https://www.home-assistant.io/docs/automation/yaml/
- Scripts: https://www.home-assistant.io/docs/scripts/
- Script actions: https://www.home-assistant.io/docs/scripts/perform-actions/
- Script conditions: https://www.home-assistant.io/docs/scripts/conditions/
- Blueprints overview: https://www.home-assistant.io/docs/blueprint/
- Blueprint schema: https://www.home-assistant.io/docs/blueprint/schema/
- Blueprint selectors: https://www.home-assistant.io/docs/blueprint/selectors/
- Template integration: https://www.home-assistant.io/integrations/template

## Repo anchors (home-assistant/home-assistant.io)

- source/_docs/automation/
- source/_docs/automation/trigger.markdown
- source/_docs/automation/condition.markdown
- source/_docs/automation/action.markdown
- source/_docs/automation/templating.markdown
- source/_docs/automation/modes.markdown
- source/_docs/automation/services.markdown
- source/_docs/automation/troubleshooting.markdown
- source/_docs/automation/yaml.markdown
- source/_docs/scripts.markdown
- source/_docs/scripts/perform-actions.markdown
- source/_docs/scripts/conditions.markdown
- source/_docs/blueprint.markdown
- source/_docs/blueprint/schema.markdown
- source/_docs/blueprint/selectors.markdown

## Key behavioral notes (short list)

- Limited-template fields in triggers (e.g., MQTT topic, webhook_id) are evaluated only at setup time.
- `for` in triggers does not survive restart or automation reload.
- `wait_template` is only re-evaluated when referenced entities change.
- Numeric state triggers fire on crossing thresholds, not when already in range.
- State triggers with only `entity_id` fire on attribute-only changes.

## Example (official docs)

Action example from the official Performing actions docs:

```yaml
action: homeassistant.turn_on
target:
  entity_id: group.living_room
```
