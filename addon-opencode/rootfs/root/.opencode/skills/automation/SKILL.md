---
name: automation
description: "Create or modify Home Assistant automations/scripts (YAML or UI-created storage) with 2024.10+ syntax (triggers/conditions/actions and action: service calls), safe entity verification, and template best practices. Use when writing new automations/scripts, converting old syntax, or producing reusable automation/script snippets."
---

# automation

## Authoring policy (native-first, low-dependency)

- Prefer native HA primitives first: use built-in trigger/condition types (`state`, `numeric_state`, `sun`, `time`, `trigger`, `and/or/not`) instead of `condition: template` when they are equivalent.
- Prefer `conditions` (or `choose` branch `conditions`) over “gate check” condition steps inside `actions` when possible. Use an action-step condition only when it must run after a delay/wait or depends on values produced by earlier actions.
- Prefer reusing existing helpers (especially `input_boolean.*` and `schedule.*`) for gating behavior instead of creating new ones. Before adding a new “mode” helper (vacation/guest/quiet-hours/etc), check whether one already exists.
- Avoid adding new dependencies (helpers/scripts) solely to eliminate a small/isolated template:
  - Create a new helper/script only if it will be reused in multiple automations.
  - If you do introduce a helper/script, favor one that generalizes well (e.g., “quiet hours”, “occupied”) and document its intended reuse.
- Templates are acceptable when they provide unique value without new dependencies, e.g.:
  - Computation (dynamic brightness/CT, clamping, math)
  - Cross-entity logic that HA can’t express cleanly without creating a new helper
  - Comparing `trigger.from_state` vs `trigger.to_state`

## Planning vs implementation (read-only research allowed)

- During planning, you may research the live Home Assistant configuration in a read-only way (entity discovery, existing automations/scripts/helpers, traces/logbook/history) to avoid guessing and avoid breaking dependencies.
- Do **not** implement changes (create/update automation/script, reload, restart, or execute services) until the user explicitly says to proceed (e.g., “implement”, “create it”, “go ahead”, “apply changes”).

## Workflow

1. (Planning) Discover exact entities/areas/groups with `ha_get_overview()` or `ha_search_entities()`.
2. (Planning) Discover relevant existing helpers and reuse them for gating:
   - Quick scan: `ha_search_entities(query="vacation", domain_filter="input_boolean")`, `ha_search_entities(query="guest", domain_filter="input_boolean")`
   - Full scan (when needed): `ha_config_list_helpers("input_boolean")`, `ha_search_entities(query="", domain_filter="schedule")`
3. (Planning) Check existing dependencies/owners before editing:
   - Find references: `ha_deep_search("<entity_id_or_service>")`
   - Read existing items: `ha_config_get_automation(...)`, `ha_config_get_script(...)`
4. (Planning) Confirm any sensitive states with `ha_get_state()` before acting.
5. (Planning) Draft automation/script using the 2024.10+ conventions in `references/yaml-style.md`.
6. (Planning) For templates, sanity-check with `ha_eval_template()` (defaults like `| int(0)`, `| float(0)`).
7. (Implementation; requires explicit user go-ahead) Create/update via:
   - Automations: `ha_config_set_automation(...)` / `ha_config_get_automation(...)`
   - Scripts: `ha_config_set_script(...)` / `ha_config_get_script(...)`
8. (Implementation; requires explicit user go-ahead) Reload: `ha_reload_core(target="automations")` or `ha_reload_core(target="scripts")` (restart only if required).
9. If behavior is wrong, inspect traces: `ha_get_automation_traces(...)` (see `references/debugging.md`).

## References

- `references/actions-schema.md` - action/sequence validation source
- `references/blueprints.md` - blueprint usage and editing guidance
- `references/checklist.md` - pre-flight checklist
- `references/debugging.md` - traces/logbook/history workflow
- `references/patterns.md` - common automation/script patterns
- `references/schema.md` - what config keys are allowed
- `references/snippets.md` - copy/paste templates
- `references/yaml-style.md` - style + 2024.10+ syntax rules
