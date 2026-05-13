---
title: Hermes Built-in Tools Reference
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [hermes, tools, reference]
sources: [raw/articles/hermes-built-in-tools.md]
---

# Hermes Built-in Tools Reference

源文档：[Hermes Built-in Tools Reference](https://hermes-agent.nousresearch.com/docs/reference/built-in-tools)

# Built-in Tools Reference

This page documents all 53 built-in tools in the Hermes tool registry, grouped by toolset. Availability varies by platform, credentials, and enabled toolsets.

**Quick counts:** 11 browser tools, 4 file tools, 10 RL tools, 4 Home Assistant tools, 2 terminal tools, 2 web tools, 5 Feishu tools, and 15 standalone tools across other toolsets.

:::tip MCP Tools
In addition to built-in tools, Hermes can load tools dynamically from MCP servers. MCP tools appear with a server-name prefix (e.g., `github_create_issue` for the `github` MCP server). See [MCP Integration](/docs/user-guide/features/mcp) for configuration.
:::

## `browser` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `browser_back` | Navigate back to the previous page in browser history. Requires browser_navigate to be called first. | — |
| `browser_cdp` | Send a raw Chrome DevTools Protocol (CDP) command. Escape hatch for browser operations not covered by browser_navigate, browser_click, browser_console, etc. Only available when a CDP endpoint is reachable at session start — via `/browser connect` or `browser.cdp_url` config. See https://chromedevtools.github.io/devtools-protocol/ | — |
| `browser_click` | Click ...

## `clarify` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `clarify` | Ask the user a question when you need clarification, feedback, or a decision before proceeding. Supports two modes: 1. **Multiple choice** — provide up to 4 choices. The user picks one or types their own answer via a 5th 'Other' option. 2.… | — |...

## `code_execution` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `execute_code` | Run a Python script that can call Hermes tools programmatically. Use this when you need 3+ tool calls with processing logic between them, need to filter/reduce large tool outputs before they enter your context, need conditional branching (… | — |...

## `cronjob` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `cronjob` | Unified scheduled-task manager. Use `action="create"`, `"list"`, `"update"`, `"pause"`, `"resume"`, `"run"`, or `"remove"` to manage jobs. Supports skill-backed jobs with one or more attached skills, and `skills=[]` on update clears attached skills. Cron runs happen in fresh sessions with no current-chat context. | — |...

## `delegation` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `delegate_task` | Spawn one or more subagents to work on tasks in isolated contexts. Each subagent gets its own conversation, terminal session, and toolset. Only the final summary is returned -- intermediate tool results never enter your context window. TWO… | — |...

## `feishu_doc` toolset

Scoped to the Feishu document-comment intelligent-reply handler (`gateway/platforms/feishu_comment.py`). Not exposed on `hermes-cli` or the regular Feishu chat adapter.

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `feishu_doc_read` | Read the full text content of a Feishu/Lark document (Docx, Doc, or Sheet) given its file_type and token. | Feishu app credentials |...

## `feishu_drive` toolset

Scoped to the Feishu document-comment handler. Drives comment read/write operations on drive files.

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `feishu_drive_add_comment` | Add a top-level comment on a Feishu/Lark document or file. | Feishu app credentials |
| `feishu_drive_list_comments` | List whole-document comments on a Feishu/Lark file, most recent first. | Feishu app credentials |
| `feishu_drive_list_comment_replies` | List replies on a specific Feishu comment thread (whole-doc or local-selection). | Feishu app credentials |
| `feishu_d...

## `file` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `patch` | Targeted find-and-replace edits in files. Use this instead of sed/awk in terminal. Uses fuzzy matching (9 strategies) so minor whitespace/indentation differences won't break it. Returns a unified diff. Auto-runs syntax checks after editing… | — |
| `read_file` | Read a text file with line numbers and pagination. Use this instead of cat/head/tail in terminal. Output format: 'LINE_NUM\|CONTENT'. Suggests similar filenames if not found. Use offset and limit for large files. NOTE: Cannot read im...

## `homeassistant` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `ha_call_service` | Call a Home Assistant service to control a device. Use ha_list_services to discover available services and their parameters for each domain. | — |
| `ha_get_state` | Get the detailed state of a single Home Assistant entity, including all attributes (brightness, color, temperature setpoint, sensor readings, etc.). | — |
| `ha_list_entities` | List Home Assistant entities. Optionally filter by domain (light, switch, climate, sensor, binary_sensor, cover, fan, etc.) or by area name (l...

## `image_gen` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `image_generate` | Generate high-quality images from text prompts using FAL.ai. The underlying model is user-configured (default: FLUX 2 Klein 9B, sub-1s generation) and is not selectable by the agent. Returns a single image URL. Display it using… | FAL_KEY |...

## `memory` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `memory` | Save important information to persistent memory that survives across sessions. Your memory appears in your system prompt at session start -- it's how you remember things about the user and your environment between conversations. WHEN TO SA… | — |...

## `messaging` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `send_message` | Send a message to a connected messaging platform, or list available targets. IMPORTANT: When the user asks to send to a specific channel or person (not just a bare platform name), call send_message(action='list') FIRST to see available tar… | — |...

## `moa` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `mixture_of_agents` | Route a hard problem through multiple frontier LLMs collaboratively. Makes 5 API calls (4 reference models + 1 aggregator) with maximum reasoning effort — use sparingly for genuinely difficult problems. Best for: complex math, advanced alg… | OPENROUTER_API_KEY |...

## `rl` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `rl_check_status` | Get status and metrics for a training run. RATE LIMITED: enforces 30-minute minimum between checks for the same run. Returns WandB metrics: step, state, reward_mean, loss, percent_correct. | TINKER_API_KEY, WANDB_API_KEY |
| `rl_edit_config` | Update a configuration field. Use rl_get_current_config() first to see all available fields for the selected environment. Each environment has different configurable options. Infrastructure settings (tokenizer, URLs, lora_rank, learning_ra… |...

## `session_search` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `session_search` | Search your long-term memory of past conversations. This is your recall -- every past session is searchable, and this tool summarizes what happened. USE THIS PROACTIVELY when: - The user says 'we did this before', 'remember when', 'last ti… | — |...

## `skills` toolset

| Tool | Description | Requires environment |
|------|-------------|----------------------|
| `skill_manage` | Manage skills (create, update, delete). Skills are your procedural memory — reusable

> 完整内容见 raw 源文件

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-bundled-skills-catalog]] — 内置skill目录
- [[hermes-optional-skills-catalog]] — 可选skill目录
