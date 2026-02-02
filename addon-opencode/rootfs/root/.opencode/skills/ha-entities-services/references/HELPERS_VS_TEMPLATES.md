# Helpers vs Templates

Prefer built-in helpers for simple logic and storage:

- Use `input_boolean` or `input_select` for stateful flags.
- Use `min_max`, `statistics`, or `utility_meter` helpers for math and tracking.
- Use `group` for any/all logic instead of a template binary sensor.

Use template entities when:

- You need derived state/attributes not covered by helpers.
- You need to normalize raw integration data.

## Example (official docs)

Template sensor example from the Template integration docs:

```yaml
template:
  - sensor:
      - name: "Average temperature"
        unit_of_measurement: "°C"
        state: >
          {% set bedroom = states('sensor.bedroom_temperature') | float %}
          {% set kitchen = states('sensor.kitchen_temperature') | float %}

          {{ ((bedroom + kitchen) / 2) | round(1, default=0) }}
```
