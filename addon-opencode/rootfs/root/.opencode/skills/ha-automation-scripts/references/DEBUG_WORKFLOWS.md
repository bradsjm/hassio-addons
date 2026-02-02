# Automation Debug Workflows

## Quick triage

1) Confirm the trigger fires: `ha_get_automation_traces`.
2) Check conditions and action errors in the trace.
3) Verify entities and services exist.

## Timeline and history

- `ha_get_logbook` for a human-readable event timeline.
- `ha_get_history` for raw state transitions.

## Reference search

- `ha_deep_search` to find automations/scripts referencing a specific entity or service.

## Example (official docs)

Template example from the State and state object docs:

```jinja2
{{ states.switch.my_switch.last_changed }}
```
