# Home Assistant integration development (official docs)

Use these links as the source of truth for platform patterns and best practices.

## Architecture and lifecycle

- Developing integrations (entry point): https://developers.home-assistant.io/docs/creating_integration_index/
- Config entries: https://developers.home-assistant.io/docs/config_entries_index/
- Config flows: https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
- Data fetching + `DataUpdateCoordinator`: https://developers.home-assistant.io/docs/integration_fetching_data/
- Entity platforms: https://developers.home-assistant.io/docs/core/entity/

## Reliability and UX

- Handling errors/retries (`ConfigEntryNotReady`, `ConfigEntryAuthFailed`, etc.): https://developers.home-assistant.io/docs/integration_setup_failures/
- Integration quality scale: https://developers.home-assistant.io/docs/quality_scale_index/
- Tests (general): https://developers.home-assistant.io/docs/development_testing/

## Practical references (code patterns)

When you need “real” examples, prefer reading current core integrations:
- `homeassistant/components/*` in https://github.com/home-assistant/core
