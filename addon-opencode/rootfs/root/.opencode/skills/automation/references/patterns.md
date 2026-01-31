# Patterns

## Motion lighting (simple)

- Trigger on motion `binary_sensor` -> `on`
- Optional conditions: sun/time window
- Action: turn on group, then delay, then turn off
- Use `mode: restart` so new motion restarts the timer

## Motion lighting (presence-aware / “only turn off what I turned on”)

- When turning on lights, store intent in a helper (e.g., `input_boolean.<area>_auto_light_on`) or use `trigger` context to decide “ownership”.
- Only turn off lights if you “own” them, to avoid shutting off lights someone manually turned on.

## Use trigger IDs to avoid duplicated logic

- Give each trigger an `id`
- Use `condition: trigger` to route behavior

## Use `choose` for time-of-day behavior

- Morning vs evening brightness/kelvin variants
- Provide a `default:` fallback

## Use `wait_for_trigger` to avoid fixed delays

- Prefer `wait_for_trigger` with `timeout` for “wait until motion off” patterns.
- Use `continue_on_timeout: false` when the next steps should only run if the wait succeeded.

## Startup cleanup (idempotent)

- Add a `homeassistant.start` trigger branch for “cleanup” only when it is safe:
  - Turn off lights *only if the area is unoccupied* or if a helper indicates the automation owns them.

## Error handling

- Use `continue_on_error: true` for non-critical notifications
- Use `stop:` for hard safety blocks (e.g., “door not open, cannot unlock”)

## Safe service calls (targets > hardcoding)

- Prefer `target:` with `area_id`, `device_id`, `label_id`, or group entities when available.
- Avoid hardcoding lists of entities unless you have a stable “fixture set” that won’t churn.
