# ESPHome + HA troubleshooting checklist

## Collect facts first

1) In Home Assistant:
   - Confirm integration exists: `ha_list_integrations(query="esphome")`
   - Find related entities: `ha_search_entities(query="<node or room name>", limit=50)`
   - Map entity → device: `ha_get_device(entity_id="...")`
2) For HA-wide regressions:
   - If present, snapshot `sensor.active_issues` before/after changes.

## Symptom: device “offline” in dashboard, but network seems fine

Checks:
- Can you ping the device IP from the network?
- Are you relying on `.local` hostnames (mDNS/ZeroConf)?

Likely causes:
- mDNS visibility issues (container networking, router multicast filtering, VLANs).
- ESPHome dashboard discovery settings/mDNS disabled.

Next actions:
- Prefer IP address during setup to bypass mDNS temporarily.
- If you’re on Docker, review known issues around mDNS discovery and any settings that disable it.

## Symptom: HA config flow says “invalid encryption key”

Checks:
- Confirm the ESPHome node firmware actually has the key you think it has (flashed after edits).
- Confirm you’re not mixing an “old” adopted config vs the current YAML/node name.

Next actions:
- Reflash the node with the desired `api.encryption.key` (USB if in doubt).
- Retry HA config flow and supply the matching key (`noise_psk` in the HA UI).

## Symptom: entity names are duplicated or messy

Checks:
- Is the per-entity `name:` repeating `${friendly_name}` or `${node_name}`?

Next actions:
- Make per-entity `name:` short; let HA/device naming provide context.
- Standardize naming via `substitutions:` and keep them consistent across nodes.

