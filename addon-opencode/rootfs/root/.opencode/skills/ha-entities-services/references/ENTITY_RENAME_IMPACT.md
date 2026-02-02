# Entity Rename Impact

Renaming an entity does **not** update references in:

- Automations and scripts
- Dashboards and cards
- Blueprints using explicit entity IDs

Recommended workflow:

1) Use `ha_deep_search` to find references.
2) Update affected automations/scripts/dashboards.
3) Rename entity after updating references.

## Example (official docs)

Entity ID format example from the State and state object docs:

```text
light.kitchen
```
