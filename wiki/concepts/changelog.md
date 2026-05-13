---
title: Changelog
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/changelog.md]
---

# Changelog

源文档：[Changelog](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)

# Changelog

## 2.1.119

- `/config` settings (theme, editor mode, verbose, etc.) now persist to `~/.claude/settings.json` and participate in project/local/policy override precedence
- Added `prUrlTemplate` setting to point the footer PR badge at a custom code-review URL instead of github.com
- Added `CLAUDE_CODE_HIDE_CWD` environment variable to hide the working directory in the startup logo
- `--from-pr` now accepts GitLab merge-request, Bitbucket pull-request, and GitHub Enterprise PR URLs
- `--print` mode now honors the agent's `tools:` and `disallowedTools:` frontmatter, matching interactive-mode behavior
- `--ag...

## 2.1.118

- Added vim visual mode (`v`) and visual-line mode (`V`) with selection, operators, and visual feedback
- Merged `/cost` and `/stats` into `/usage` — both remain as typing shortcuts that open the relevant tab
- Create and switch between named custom themes from `/theme`, or hand-edit JSON files in `~/.claude/themes/`; plugins can also ship themes via a `themes/` directory
- Hooks can now invoke MCP tools directly via `type: "mcp_tool"`
- Added `DISABLE_UPDATES` env var to completely block all update paths including manual `claude update` — stricter than `DISABLE_AUTOUPDATER`
- WSL on Windows c...

## 2.1.117

- Forked subagents can now be enabled on external builds by setting `CLAUDE_CODE_FORK_SUBAGENT=1`
- Agent frontmatter `mcpServers` are now loaded for main-thread agent sessions via `--agent`
- Improved `/model`: selections now persist across restarts even when the project pins a different model, and the startup header shows when the active model comes from a project or managed-settings pin
- The `/resume` command now offers to summarize stale, large sessions before re-reading them, matching the existing `--resume` behavior
- Faster startup when both local and claude.ai MCP servers are configur...

## 2.1.116

- `/resume` on large sessions is significantly faster (up to 67% on 40MB+ sessions) and handles sessions with many dead-fork entries more efficiently
- Faster MCP startup when multiple stdio servers are configured; `resources/templates/list` is now deferred to first `@`-mention
- Smoother fullscreen scrolling in VS Code, Cursor, and Windsurf terminals — `/terminal-setup` now configures the editor's scroll sensitivity
- Thinking spinner now shows progress inline ("still thinking", "thinking more", "almost done thinking"), replacing the separate hint row
- `/config` search now matches option val...

## 2.1.114

- Fixed a crash in the permission dialog when an agent teams teammate requested tool permission...

## 2.1.113

- Changed the CLI to spawn a native Claude Code binary (via a per-platform optional dependency) instead of bundled JavaScript
- Added `sandbox.network.deniedDomains` setting to block specific domains even when a broader `allowedDomains` wildcard would otherwise permit them
- Fullscreen mode: Shift+↑/↓ now scrolls the viewport when extending a selection past the visible edge
- `Ctrl+A` and `Ctrl+E` now move to the start/end of the current logical line in multiline input, matching readline behavior
- Windows: `Ctrl+Backspace` now deletes the previous word
- Long URLs in responses and bash output...

## 2.1.112

- Fixed "claude-opus-4-7 is temporarily unavailable" for auto mode...

## 2.1.111

- Claude Opus 4.7 xhigh is now available! Use /effort to tune speed vs. intelligence
- Auto mode is now available for Max subscribers when using Opus 4.7
- Added `xhigh` effort level for Opus 4.7, sitting between `high` and `max`. Available via `/effort`, `--effort`, and the model picker; other models fall back to `high`
- `/effort` now opens an interactive slider when called without arguments, with arrow-key navigation between levels and Enter to confirm
- Added "Auto (match terminal)" theme option that matches your terminal's dark/light mode — select it from `/theme`
- Added `/less-permissio...

## 2.1.110

- Added `/tui` command and `tui` setting — run `/tui fullscreen` to switch to flicker-free rendering in the same conversation
- Added push notification tool — Claude can send mobile push notifications when Remote Control and "Push when Claude decides" config are enabled
- Changed `Ctrl+O` to toggle between normal and verbose transcript only; focus view is now toggled separately with the new `/focus` command
- Added `autoScrollEnabled` config to disable conversation auto-scroll in fullscreen mode
- Added option to show Claude's last response as commented context in the `Ctrl+G` external editor ...

## 2.1.109

- Improved the extended-thinking indicator with a rotating progress hint...

## 2.1.108

- Added `ENABLE_PROMPT_CACHING_1H` env var to opt into 1-hour prompt cache TTL on API key, Bedrock, Vertex, and Foundry (`ENABLE_PROMPT_CACHING_1H_BEDROCK` is deprecated but still honored), and `FORCE_PROMPT_CACHING_5M` to force 5-minute TTL
- Added recap feature to provide context when returning to a session, configurable in `/config` and manually invocable with `/recap`; force with `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` if telemetry disabled.
- The model can now discover and invoke built-in slash commands like `/init`, `/review`, and `/security-review` via the Skill tool
- `/undo` is now an alias...

## 2.1.107

- Show thinking hints sooner during long operations...

## 2.1.105

- Added `path` parameter to the `EnterWorktree` tool to switch into an existing worktree of the current repository
- Added PreCompact hook support: hooks can now block compaction by exiting with code 2 or returning `{"decision":"block"}`
- Added background monitor support for plugins via a top-level `monitors` manifest key that auto-arms at session start or on skill invoke
- `/proactive` is now an alias for `/loop`
- Improved stalled API stream handling: streams now abort after 5 minutes of no data and retry non-streaming instead of hanging indefinitely
- Improved network error messages: conne...

## 2.1.101

- Added `/team-onboarding` command to generate a teammate ramp-up guide from your local Claude Code usage
- Added OS CA certificate store trust by default, so enterprise TLS proxies work without extra setup (set `CLAUDE_CODE_CERT_STORE=bundled` to use only bundled CAs)
- `/ultraplan` and other remote-session features now auto-create a default cloud environment instead of requiring web setup first
- Improved brief mode to retry once when Claude responds with plain text instead of a structured message
- Improved focus mode: Claude now writes more self-contained summaries since it knows you only ...

## 2.1.98

- Added interactive Google Vertex AI setup wizard accessible from the login screen when selecting "3rd-party platform", guiding you through GCP authentication, project and region configuration, credential verification, and model pinning
- Added `CLAUDE_CODE_PERFORCE_MODE` env var: when set, Edit/Write/NotebookEdit fail on read-only files with a `p4 edit` hint instead of silently overwriting them
- Added Monitor tool for streaming events from background scripts
- Added subprocess sandboxing with PID namespace isolation on Linux when `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` is set, and `CLAUDE_CODE_SC...

## 2.1.97

- Added focus view toggle (`Ctrl+O`) in `NO_FLICKER` mode showing prompt, one-line tool summary with edit diffstats, and final response
- Added `refreshInterval` status line setting to re-run the status line command every N seconds
- Added `workspace.git_worktree` to the status line JSON input, set when the current directory is inside a linked git worktree
- Added `● N running` indicator in `/agents` next to agent types with live subagent instances
- Added syntax highlighting for Cedar policy files (`.cedar`, `.cedarpolicy`)
- Fixed `--dangerously-skip-permissions` being silently downgraded to...

## 2.1.96

- Fixed Bedrock requests failing with `403 "Authorization header is missing"` when using `AWS_BEARER_TOKEN_BEDROCK` or `CLAUDE_CODE_SKIP_BEDROCK_AUTH` (regression in 2.1.94)...

## 2.1.94

- Added support for Amazon Bedroc

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
