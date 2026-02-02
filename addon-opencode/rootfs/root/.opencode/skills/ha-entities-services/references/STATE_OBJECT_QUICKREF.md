# State Object Quick Reference

## State object fields

- `state.state`: the entity state string
- `state.entity_id`: `<domain>.<object_id>`
- `state.attributes`: dictionary of extra attributes
- `state.last_changed`: changes to state only
- `state.last_updated`: changes to state or attributes
- `state.last_reported`: any write to the state machine

## Template guidance

- Prefer `states('sensor.x')` over `states.sensor.x.state` to avoid missing-entity errors.

## Example (official docs)

From the State and state object docs:

```jinja2
{{ states.switch.my_switch.last_changed }}
```
