# Limited Templates Quick Reference

Limited templates are used in some trigger fields and in `trigger_variables`. They only support a subset of Home Assistant template extensions.

## Commonly unsupported in limited templates

- `states` object iteration/access helpers and related shortcuts
- Attribute helpers and `state_attr`/`is_state_attr`
- Group expansion via `expand`
- `state_translated`
- `distance()` and `closest()`
- `device_attr()` / `is_device_attr()`
- `config_entry_attr()`
- Time helpers: `now()`, `utcnow()`, `time_since()`, `time_until()`, `today_at()`

## Practical guidance

- If a template works in an action/condition but fails in a trigger field, it is likely limited-template related.
- Move complex logic into a condition or a template entity when possible.
- Use `ha_eval_template` to validate in the correct context.

## Example (official docs)

State access example from the official Templating docs (not valid in limited templates):

```jinja2
{{ states('device_tracker.paulus') }}
```
