# Snippets

## Skeleton automation (2024.10+)

```yaml
automation:
  - id: example_automation_v1
    alias: Example Automation
    description: "What this automation does and why."
    mode: single
    triggers:
      - trigger: state
        entity_id: binary_sensor.example
        to: "on"
        id: example_trigger
    actions:
      - alias: "Do something"
        action: persistent_notification.create
        data:
          title: "Example"
          message: "Triggered by {{ trigger.entity_id }}"

## Choose (time-of-day branches)

```yaml
automation:
  - id: example_choose_v1
    alias: Example Choose
    triggers:
      - trigger: state
        entity_id: binary_sensor.example_motion
        to: "on"
    actions:
      - choose:
          - conditions:
              - condition: state
                entity_id: sun.sun
                state: "below_horizon"
            sequence:
              - action: light.turn_on
                target:
                  entity_id: light.example
                data:
                  brightness_pct: 15
        default:
          - action: light.turn_on
            target:
              entity_id: light.example
            data:
              brightness_pct: 80
```

## Wait for trigger (no fixed delay)

```yaml
automation:
  - id: example_wait_v1
    alias: Example Wait For Motion Off
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.example_motion
        to: "on"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.example
      - wait_for_trigger:
          - trigger: state
            entity_id: binary_sensor.example_motion
            to: "off"
        timeout: "00:05:00"
        continue_on_timeout: false
      - action: light.turn_off
        target:
          entity_id: light.example
```

## Skeleton script

```yaml
script:
  example_script:
    alias: Example Script
    description: "What this script does."
    mode: single
    sequence:
      - action: persistent_notification.create
        data:
          title: "Example"
          message: "Hello"
```
