# Action/sequence schema (source-of-truth)

Automations and scripts share the same “action sequence” engine.

## Source-of-truth

Home Assistant Core:
- Action engine + validation lives in `homeassistant/helpers/script.py`
- Automation config plugs this in via `script.make_script_schema(...)` in `homeassistant/components/automation/config.py`

When you are unsure whether a key is valid inside `actions:` / `sequence:`, trust core.

## Practical guidance

- Prefer the **modern** syntax shown in the official docs:
  - Automation actions: https://www.home-assistant.io/docs/automation/action/
  - Performing actions: https://www.home-assistant.io/docs/scripts/perform-actions/
- When editing existing automations/scripts, keep the existing style unless you are deliberately migrating it.
- If Home Assistant rejects a config update, the error is a schema validation error: remove/rename unsupported keys rather than “guessing” new ones.

## Common action types (non-exhaustive)

The action engine supports many action forms, including:
- Service/perform-action calls
- `choose`
- `if` / `then` / `else`
- `repeat`
- `wait_for_trigger`
- `wait_template`
- `delay`
- `stop`

For the definitive list and current syntax, use the official docs links above and consult `homeassistant/helpers/script.py`.
