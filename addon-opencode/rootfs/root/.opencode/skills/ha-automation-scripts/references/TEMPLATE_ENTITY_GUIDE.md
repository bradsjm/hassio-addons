# Template Entities and Trigger-Based Templates

## When to use template entities

- You need derived values that can be referenced safely by automations.
- You want to avoid limited-template restrictions in triggers.

## Trigger-based template entities

- Only update when their triggers fire.
- Do not re-render on referenced state changes unless you add explicit state triggers.
- Sensors and binary sensors restore state after restart; other trigger-based entities do not.

## Variables

- State-based template variables resolve on config load/reload.
- Trigger-based template variables resolve between triggers and actions.

## Example (official docs)

Trigger-based template sensor example from the Template integration docs:

```yaml
template:
  - triggers:
      - trigger: time_pattern
        hours: 0
        minutes: 0
    sensor:
      - name: "Not smoking"
        state: '{{ ((as_timestamp(now()) - as_timestamp(strptime("06.07.2018", "%d.%m.%Y"))) / 86400) | round(default=0) }}'
        unit_of_measurement: "Days"
```
