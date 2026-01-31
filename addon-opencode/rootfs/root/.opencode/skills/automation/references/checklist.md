# Checklist (before creating/updating)

- Entity IDs verified via `ha_search_entities()` or `ha_get_overview()`
- Checked for relevant existing helpers to reuse (avoid duplicating “mode” toggles): `ha_search_entities(query="vacation", domain_filter="input_boolean")`, `ha_search_entities(query="guest", domain_filter="input_boolean")`, `ha_config_list_helpers("input_boolean")`, `ha_search_entities(query="", domain_filter="schedule")`
- Sensitive device states confirmed with `ha_get_state()`
- If the user has not asked to proceed yet: stop after producing the proposed config/diff and ask for explicit confirmation before calling any write actions (create/update/reload/service calls)
- Uses 2024.10+ keys: `triggers/conditions/actions` and step `action:`
- If adding fields, confirm they exist in the automation schema (see `schema.md`); unsupported keys will fail validation.
- Templates quoted and safe-cast with defaults (`| int(0)`, `| float(0)`)
- Prefer `conditions` / `choose` branch `conditions` over inline “gate check” condition steps at the start of a `sequence`
- Replace `condition: template` with native condition types when equivalent (`state`, `numeric_state`, `sun`, `time`, `trigger`, `and/or/not`)
- Do not add new helpers/scripts solely to remove templates unless reused in **3+ automations** (or clearly intended as a house-wide primitive)
- If any template remains, add an `alias` explaining why a native condition isn’t sufficient without adding dependencies
- `id` is stable and unique (underscores only)
- Reload targeted component via `ha_reload_core(target=...)`
- If debugging needed: inspect traces/logbook/history (see `debugging.md`)
