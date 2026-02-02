# Dashboard Design Patterns (Native-First)

## Layout choices

- Use `type: sections` for modern, maintainable layouts.
- Keep sections aligned to areas/rooms for easy navigation.
- Use `grid` cards inside sections for dense clusters.

## Card selection

- Default to `tile` for controls and sensors.
- Use `heading` for section titles and quick scanning.
- Use `conditional` for swapping cards by state instead of templating fields.

## Dynamic UI without templates

- Do not use Jinja in Lovelace YAML.
- Create template entities for derived values, then display them normally.
- Use `visibility` for simple show/hide rules.

## Accessibility and usability

- Keep 2-3 columns for desktop and avoid overloading mobile views.
- Put high-frequency actions near the top of the view.

## Example (official docs)

Sections view type from the official Sections docs:

```yaml
type: sections
```
