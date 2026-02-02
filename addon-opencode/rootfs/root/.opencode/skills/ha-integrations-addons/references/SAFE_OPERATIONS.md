# Safe Operations

## Avoid destructive changes

- Disabling is safer than deleting config entries.
- Deleting config entries may remove devices and entities.

## Prefer reloads

- Use `ha_reload_core` for automations, scripts, or helpers when possible.
- Only use `ha_restart` after `ha_check_config`.

## Example (official docs)

Action example from the Performing actions docs:

```yaml
action: homeassistant.turn_on
target:
  entity_id: group.living_room
```
