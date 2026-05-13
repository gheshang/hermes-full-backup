---
title: Adding a Platform Adapter
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-adding-platform-adapters.md]
---

# Adding a Platform Adapter

源文档：[Adding a Platform Adapter](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/adding-platform-adapters.md)

# Adding a Platform Adapter

This guide covers adding a new messaging platform to the Hermes gateway. A platform adapter connects Hermes to an external messaging service (Telegram, Discord, WeCom, etc.) so users can interact with the agent through that service.

:::tip
Adding a platform adapter touches 20+ files across code, config, and docs. Use this guide as a checklist — the adapter file itself is typically only 40% of the work.
:::

## Architecture Overview

```
User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent
```

Every adapter extends `BasePlatformAdapter` from `gateway/platforms/base.py` and implements:

- **`connect()`** — Establish connection (WebSocket, long-poll, HTTP server, etc.)
- **`disconnect()`** — Clean shutdown
- **`send()`** — Send a text message to a chat
- **`send_typing()`** — Show typing indicator (optional)
- **`get_chat_info()`** — Return chat metadata

Inbound messages are received by the adapter and forwarded via `self.handle_message(event)`, which the base class routes to the gateway runner....

## Step-by-Step Checklist

### 1. Platform Enum

Add your platform to the `Platform` enum in `gateway/config.py`:

```python
class Platform(str, Enum):
    # ... existing platforms ...
    NEWPLAT = "newplat"
```

### 2. Adapter File

Create `gateway/platforms/newplat.py`:

```python
from gateway.config import Platform, PlatformConfig
from gateway.platforms.base import (
    BasePlatformAdapter, MessageEvent, MessageType, SendResult,
)

def check_newplat_requirements() -> bool:
    """Return True if dependencies are available."""
    return SOME_SDK_AVAILABLE

class NewPlatAdapter(BasePlatformAdapter):
    def __init__(...

## Parity Audit

Before marking a new platform PR as complete, run a parity audit against an established platform:

```bash
# Find every .py file mentioning the reference platform
search_files "bluebubbles" output_mode="files_only" file_glob="*.py"

# Find every .py file mentioning the new platform
search_files "newplat" output_mode="files_only" file_glob="*.py"

# Any file in the first set but not the second is a potential gap
```

Repeat for `.md` and `.ts` files. Investigate each gap — is it a platform enumeration (needs updating) or a platform-specific reference (skip)?...

## Common Patterns

### Long-Poll Adapters

If your adapter uses long-polling (like Telegram or Weixin), use a polling loop task:

```python
async def connect(self):
    self._poll_task = asyncio.create_task(self._poll_loop())
    self._mark_connected()

async def _poll_loop(self):
    while self._running:
        messages = await self._fetch_updates()
        for msg in messages:
            await self.handle_message(self._build_event(msg))
```

### Callback/Webhook Adapters

If the platform pushes messages to your endpoint (like WeCom Callback), run an HTTP server:

```python
async def connect(self):
    self._...

## Reference Implementations

| Adapter | Pattern | Complexity | Good reference for |
|---------|---------|------------|-------------------|
| `bluebubbles.py` | REST + webhook | Medium | Simple REST API integration |
| `weixin.py` | Long-poll + CDN | High | Media handling, encryption |
| `wecom_callback.py` | Callback/webhook | Medium | HTTP server, AES crypto, multi-app |
| `telegram.py` | Long-poll + Bot API | High | Full-featured adapter with groups, threads |...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
