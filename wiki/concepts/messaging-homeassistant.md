---
title: Home Assistant Integration
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-homeassistant.md]
---

# Home Assistant Integration

源文档：[Home Assistant Integration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/homeassistant.md)

# Home Assistant Integration

Hermes Agent integrates with [Home Assistant](https://www.home-assistant.io/) in two ways:

1. **Gateway platform** — subscribes to real-time state changes via WebSocket and responds to events
2. **Smart home tools** — four LLM-callable tools for querying and controlling devices via the REST API

## Setup

### 1. Create a Long-Lived Access Token

1. Open your Home Assistant instance
2. Go to your **Profile** (click your name in the sidebar)
3. Scroll to **Long-Lived Access Tokens**
4. Click **Create Token**, give it a name like "Hermes Agent"
5. Copy the token

### 2. Configure Environment Variables

```bash
# Add to ~/.hermes/.env

# Required: your Long-Lived Access Token
HASS_TOKEN=your-long-lived-access-token

# Optional: HA URL (default: http://homeassistant.local:8123)
HASS_URL=http://192.168.1.100:8123
```

:::info
The `homeassistant` toolset is automatically enabled when `HASS_TOKEN` is s...

## Available Tools

Hermes Agent registers four tools for smart home control:

### `ha_list_entities`

List Home Assistant entities, optionally filtered by domain or area.

**Parameters:**
- `domain` *(optional)* — Filter by entity domain: `light`, `switch`, `climate`, `sensor`, `binary_sensor`, `cover`, `fan`, `media_player`, etc.
- `area` *(optional)* — Filter by area/room name (matches against friendly names): `living room`, `kitchen`, `bedroom`, etc.

**Example:**
```
List all lights in the living room
```

Returns entity IDs, states, and friendly names.

### `ha_get_state`

Get detailed state of a single ent...

## Gateway Platform: Real-Time Events

The Home Assistant gateway adapter connects via WebSocket and subscribes to `state_changed` events. When a device state changes and matches your filters, it's forwarded to the agent as a message.

### Event Filtering

:::warning Required Configuration
By default, **no events are forwarded**. You must configure at least one of `watch_domains`, `watch_entities`, or `watch_all` to receive events. Without filters, a warning is logged at startup and all state changes are silently dropped.
:::

Configure which events the agent sees in `~/.hermes/config.yaml` under the Home Assistant platform's `extr...

## Security

The Home Assistant tools enforce security restrictions:

:::warning Blocked Domains
The following service domains are **blocked** to prevent arbitrary code execution on the HA host:

- `shell_command` — arbitrary shell commands
- `command_line` — sensors/switches that execute commands
- `python_script` — scripted Python execution
- `pyscript` — broader scripting integration
- `hassio` — addon control, host shutdown/reboot
- `rest_command` — HTTP requests from HA server (SSRF vector)

Attempting to call services in these domains returns an error.
:::

Entity IDs are validated against the patter...

## Example Automations

### Morning Routine

```
User: Start my morning routine

Agent:
1. ha_call_service(domain="light", service="turn_on",
     entity_id="light.bedroom", data={"brightness": 128})
2. ha_call_service(domain="climate", service="set_temperature",
     entity_id="climate.thermostat", data={"temperature": 22})
3. ha_call_service(domain="media_player", service="turn_on",
     entity_id="media_player.kitchen_speaker")
```

### Security Check

```
User: Is the house secure?

Agent:
1. ha_list_entities(domain="binary_sensor")
     → checks door/window sensors
2. ha_get_state(entity_id="alarm_control_panel....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
