# Home Assistant Automations & Scripts Reference

## Primary documentation

- Automations overview: https://www.home-assistant.io/docs/automation/
- Automation triggers: https://www.home-assistant.io/docs/automation/trigger/
- Automation conditions: https://www.home-assistant.io/docs/automation/condition/
- Automation actions: https://www.home-assistant.io/docs/automation/action/
- Automation templating: https://www.home-assistant.io/docs/automation/templating/
- Templating (Jinja + limited templates): https://www.home-assistant.io/docs/configuration/templating/
- State object model: https://www.home-assistant.io/docs/configuration/state_object/
- Automation run modes: https://www.home-assistant.io/docs/automation/modes/
- Automation actions (services): https://www.home-assistant.io/docs/automation/services/
- Troubleshooting automations: https://www.home-assistant.io/docs/automation/troubleshooting/
- Automation YAML: https://www.home-assistant.io/docs/automation/yaml/
- Scripts: https://www.home-assistant.io/docs/scripts/
- Script actions: https://www.home-assistant.io/docs/scripts/perform-actions/
- Script conditions: https://www.home-assistant.io/docs/scripts/conditions/
- Blueprints overview: https://www.home-assistant.io/docs/blueprint/
- Blueprint schema: https://www.home-assistant.io/docs/blueprint/schema/
- Blueprint selectors: https://www.home-assistant.io/docs/blueprint/selectors/
- Template integration: https://www.home-assistant.io/integrations/template

## Repo anchors (home-assistant/home-assistant.io)

- source/_docs/automation/
- source/_docs/automation/trigger.markdown
- source/_docs/automation/condition.markdown
- source/_docs/automation/action.markdown
- source/_docs/automation/templating.markdown
- source/_docs/automation/modes.markdown
- source/_docs/automation/services.markdown
- source/_docs/automation/troubleshooting.markdown
- source/_docs/automation/yaml.markdown
- source/_docs/scripts.markdown
- source/_docs/scripts/perform-actions.markdown
- source/_docs/scripts/conditions.markdown
- source/_docs/blueprint.markdown
- source/_docs/blueprint/schema.markdown
- source/_docs/blueprint/selectors.markdown

## Example (official docs)

Action example from the official Performing actions docs:

```yaml
action: homeassistant.turn_on
target:
  entity_id: group.living_room
```
