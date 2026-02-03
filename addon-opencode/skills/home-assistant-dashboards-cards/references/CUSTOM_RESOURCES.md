# Custom Resources (HACS or /local)

## When to use

- Only when built-in cards cannot meet the requirement.
- User explicitly asks for a custom card or custom styling.

## Resource checklist

- Install via HACS (preferred) or place file in `/config/www`.
- Register resource with type `module` for modern cards.
- Hard refresh browser after changes.

## Common paths

- `/hacsfiles/<repo>/<file>.js`
- `/local/<file>.js`

## Example (official docs)

Conditional card example from the official Conditional card docs:

```yaml
type: conditional
conditions:
  - condition: state
    entity: light.bed_light
    state: "on"
card:
  type: entities
  entities:
    - light.bed_light
```
