---
title: App-Specific Managed Proxy Implementation Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-03-11-app-specific-managed-proxy.md]
---

# App-Specific Managed Proxy Implementation Plan

源文档：[App-Specific Managed Proxy Implementation Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-11-app-specific-managed-proxy.md)

# App-Specific Managed Proxy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make proxy feel app-specific in TUI: `Claude`, `Codex`, and `Gemini` each get their own on/off state and current-app control, while `OpenCode` stays out if upstream does not support proxy.

**Architecture:** Keep one shared local proxy runtime, not three separate daemons. App independence lives in per-app takeover state and TUI behavior: starting proxy for the current app should either boot the managed runtime or attach the current app to an already-running managed runtime, and stopping should only tear the runtime down when no supported app is still attached. This stays close to upstream, avoids extra ports/processes, and m

## Product Guardrails

- Keep the homepage as one current-app proxy card, not a three-panel control center.
- `P` always means “toggle proxy for the current app”.
- `Claude`, `Codex`, and `Gemini` support this flow.
- `OpenCode` does not show proxy controls if upstream still treats it as unsupported.
- Do not introduce per-app proxy ports or multiple long-lived proxy daemons.
- Do not add automatic failover, queue controls, or breaker tuning....

## Current Findings

- Upstream still treats `OpenCode` proxy as unsupported in `/.upstream/cc-switch/src-tauri/src/services/proxy.rs:213` and `/.upstream/cc-switch/src-tauri/src/services/proxy.rs:376`.
- Our current backend already stores takeover state per app, but `set_managed_session_for_app()` still behaves like a single-app start/stop flow.
- The main TUI bug is semantic: if a managed runtime is already up for another app, the current app cannot cleanly “join” it from the homepage....

## Working Model For This Plan

- There is one shared managed proxy runtime.
- Each supported app has its own takeover flag and its own homepage state.
- Turning proxy on for the current app:
  - starts the managed runtime if it is not running
  - otherwise reuses the managed runtime and only enables takeover for the current app
- Turning proxy off for the current app:
  - restores that app from takeover
  - stops the managed runtime only if no supported app is still attached

---

### Task 1: Let A Second App Reuse The Existing Managed Runtime

**Files:**
- Modify: `src-tauri/src/services/proxy.rs`
- Test: `src-tauri/tests/...

## Final Verification

Run in sequence:

1. `cargo fmt`
2. `cargo test --test proxy_service -- --nocapture`
3. `cargo test --test proxy_takeover -- --nocapture`
4. `cargo test home_proxy_dashboard_ -- --nocapture`
5. `cargo test main_proxy_action -- --nocapture`
6. `cargo build --bin cc-switch`

Expected: PASS....

## Explicitly Deferred

- Separate proxy daemon per app
- Separate listen port per app
- Same-screen three-app dashboard
- `OpenCode` proxy support before upstream has it
- New CLI product surface for per-app proxy management outside TUI...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
