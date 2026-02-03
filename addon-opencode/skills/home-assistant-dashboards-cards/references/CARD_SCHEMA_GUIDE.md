# Card Schema Guide

Use these tools to avoid guessing card fields:

- `ha_get_card_types()` to list supported card types.
- `ha_get_card_documentation("<type>")` to view options for a specific card.

## Practical rule

If unsure about a card option, query the card documentation instead of copying from blogs or older YAML.

## Example (official docs)

Tile card example from the official Tile card docs:

```yaml
type: tile
entity: light.bedroom
icon: mdi:lamp
color: yellow
```
