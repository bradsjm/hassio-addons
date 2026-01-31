# Debugging workflow

## Official docs

- Troubleshooting automations (traces, testing, templates): https://www.home-assistant.io/docs/automation/troubleshooting

## Automation doesn’t trigger

1. Check entity changes: `ha_get_history(entity_ids="...")`
2. Check logbook: `ha_get_logbook(hours_back=24, entity_id="...")`
3. Confirm the automation is enabled and configured: `ha_config_get_automation("automation.x")`

## Automation triggers but does the wrong thing

1. Pull recent traces: `ha_get_automation_traces("automation.x")`
2. Get one `run_id` and re-fetch full trace for condition/action details

## Template issues

- Evaluate quickly: `ha_eval_template("{{ ... }}")`
- Add defaults: `| int(0)`, `| float(0)`, `| default(...)`
