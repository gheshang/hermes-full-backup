---
title: Features Overview
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-overview.md]
---

# Features Overview

源文档：[Features Overview](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/overview.md)

# Features Overview

Hermes Agent includes a rich set of capabilities that extend far beyond basic chat. From persistent memory and file-aware context to browser automation and voice conversations, these features work together to make Hermes a powerful autonomous assistant.

## Core

- **[Tools & Toolsets](tools.md)** — Tools are functions that extend the agent's capabilities. They're organized into logical toolsets that can be enabled or disabled per platform, covering web search, terminal execution, file editing, memory, delegation, and more.
- **[Skills System](skills.md)** — On-demand knowledge documents the agent can load when needed. Skills follow a progressive disclosure pattern to minimize token usage and are compatible with the [agentskills.io](https://agentskills.io/specification) open standard.
- **[Persistent Memory](memory.md)** — Bounded, curated memory that ...

## Automation

- **[Scheduled Tasks (Cron)](cron.md)** — Schedule tasks to run automatically with natural language or cron expressions. Jobs can attach skills, deliver results to any platform, and support pause/resume/edit operations.
- **[Subagent Delegation](delegation.md)** — The `delegate_task` tool spawns child agent instances with isolated context, restricted toolsets, and their own terminal sessions. Run 3 concurrent subagents by default (configurable) for parallel workstreams.
- **[Code Execution](code-execution.md)** — The `execute_code` tool lets the agent write Python scripts that call Hermes tool...

## Media & Web

- **[Voice Mode](voice-mode.md)** — Full voice interaction across CLI and messaging platforms. Talk to the agent using your microphone, hear spoken replies, and have live voice conversations in Discord voice channels.
- **[Browser Automation](browser.md)** — Full browser automation with multiple backends: Browserbase cloud, Browser Use cloud, local Chrome via CDP, or local Chromium. Navigate websites, fill forms, and extract information.
- **[Vision & Image Paste](vision.md)** — Multimodal vision support. Paste images from your clipboard into the CLI and ask the agent to analyze, describe, or ...

## Integrations

- **[MCP Integration](mcp.md)** — Connect to any MCP server via stdio or HTTP transport. Access external tools from GitHub, databases, file systems, and internal APIs without writing native Hermes tools. Includes per-server tool filtering and sampling support.
- **[Provider Routing](provider-routing.md)** — Fine-grained control over which AI providers handle your requests. Optimize for cost, speed, or quality with sorting, whitelists, blacklists, and priority ordering.
- **[Fallback Providers](fallback-providers.md)** — Automatic failover to backup LLM providers when your primary model encount...

## Customization

- **[Personality & SOUL.md](personality.md)** — Fully customizable agent personality. `SOUL.md` is the primary identity file — the first thing in the system prompt — and you can swap in built-in or custom `/personality` presets per session.
- **[Skins & Themes](skins.md)** — Customize the CLI's visual presentation: banner colors, spinner faces and verbs, response-box labels, branding text, and the tool activity prefix.
- **[Plugins](plugins.md)** — Add custom tools, hooks, and integrations without modifying core code. Three plugin types: general plugins (tools/hooks), memory providers (cross-s...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
