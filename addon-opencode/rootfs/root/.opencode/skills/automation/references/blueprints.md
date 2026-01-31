# Blueprints (automation) — usage patterns

## When to use a blueprint

Blueprints are a good fit when:
- You want a standardized automation pattern across many rooms/devices.
- You want to reuse the same structure and just supply different inputs.
- You want a UI-friendly configuration surface.

Avoid blueprints when:
- The automation is highly bespoke and would require many optional inputs.
- You expect constant per-room divergence over time.

## Editing guidance

- Prefer reading the automation first to see whether it is blueprint-backed:
  - `ha_config_get_automation("automation.x")` and look for `use_blueprint`.
- Blueprint-based automations can be updated by supplying a `use_blueprint` config with updated inputs, but UI edits are often the simplest path for complex changes.

## Official docs

- Blueprints: https://www.home-assistant.io/docs/blueprint/
- Automation YAML: https://www.home-assistant.io/docs/automation/yaml/
