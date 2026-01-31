# Home Assistant YAML authoring (2024.10+)

## Required fields (automations)

- `id`: unique (alphanumeric + underscores), stable over time
- `alias`: human-friendly name
- `triggers`: list (even if 1 item)
- `actions`: list (even if 1 item)

## Required fields (scripts)

- `sequence`: list of actions
- Prefer adding `alias` and `description`

## Syntax rules (2024.10+)

- Top-level keys: `triggers:`, `conditions:`, `actions:` (plural)
- Inside each trigger item: `trigger:` (singular)
- Prefer modern action syntax in steps: `action: <domain.service>` (recommended by current docs).
  - Many existing configs still use legacy `service:` syntax; keep existing style unless migrating, and validate after edits (see `references/actions-schema.md`).

## Formatting rules

- 2 spaces indentation
- Quote single-line templates: `"{{ ... }}"`
- Use defaults for unsafe conversions:
  - `"{{ states('sensor.x') | float(0) }}"`
  - `"{{ states('input_number.y') | int(0) }}"`
- Quote string states: `"on"`, `"off"`, `"home"`, `"away"`

## Template minimization (native-first, no-new-helper by default)

- Do not use `condition: template` when an equivalent exists using built-in conditions (`state`, `numeric_state`, `sun`, `time`, `trigger`, `and/or/not`).
- Do not create new helpers/scripts solely to eliminate templates unless they will be reused in **3+ automations** (or are clearly intended as a house-wide primitive).
- Prefer putting gating logic in `conditions:` / `choose:` `conditions:` rather than as “gate check” condition steps at the top of an action `sequence:`. Keep action-step conditions only when they must occur after a `delay`/`wait_for_trigger` or depend on outputs from earlier actions.

Common replacements:

- Night/day checks:
  - Prefer `condition: state` on `sun.sun` (`below_horizon` / `above_horizon`) over `{{ is_state('sun.sun', ...) }}` templates.
- Quiet-hours checks:
  - Prefer `condition: state` on a `schedule.*` helper over `{{ is_state('schedule.*', 'on') }}` templates.
- Composite “gate” templates:
  - Prefer multiple native conditions (one per entity) over a single `{{ a and b and c }}` template gate.

When templates are appropriate:

- Dynamic computation (e.g., CT/brightness math).
- Cross-entity logic that would otherwise require creating a new helper just for one automation.

## Entity safety

- Never guess `entity_id`. Always verify with `ha_search_entities()` / `ha_get_overview()`.
- Prefer group/area targets when available.

## Official docs (quick links)

- Automations overview: https://www.home-assistant.io/docs/automation/
- Automation basics: https://www.home-assistant.io/docs/automation/basics
- Automation YAML: https://www.home-assistant.io/docs/automation/yaml/
- Triggers: https://www.home-assistant.io/docs/automation/trigger/
- Conditions: https://www.home-assistant.io/docs/automation/condition/
- Actions: https://www.home-assistant.io/docs/automation/action/
- Script syntax: https://www.home-assistant.io/docs/scripts/
- Performing actions (targets/data/response): https://www.home-assistant.io/docs/scripts/perform-actions/
- Templating (Jinja helpers, areas/devices/labels): https://www.home-assistant.io/docs/configuration/templating/
