---
title: Proxy Phase C Manual Takeover Implementation Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-03-10-proxy-phase-c-manual-takeover.md]
---

# Proxy Phase C Manual Takeover Implementation Plan

源文档：[Proxy Phase C Manual Takeover Implementation Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-10-proxy-phase-c-manual-takeover.md)

# Proxy Phase C Manual Takeover Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Move the local proxy from a Phase B foreground debug server to an upstream-shaped manual takeover runtime, without adding automatic failover.

**Architecture:** Keep the existing multi-app proxy routes and per-app timeout/retry behavior, but pull the runtime boundary closer to upstream by introducing `handler_context`, `provider_router`, and response pipeline helpers. Add per-app takeover and restore as explicit service actions only. TUI stays thin: show status, show takeover state, and expose only the minimum manual controls.

**Tech Stack:** Rust, tokio, axum, reqwest, rusqlite, clap, ratatui.

---

## Scope Guardrails

- Do not implement automatic failover.
- Do not route across provider queues.
- Do not add failover queue editing to CLI or TUI.
- Do not add tray or GUI-specific runtime behavior.
- Keep `auto_failover_enabled` as a stored compatibility field only.
- Prefer upstream naming and file boundaries when they fit the CLI repo....

## Runtime Model

- No daemon in this phase.
- Manual takeover is only valid while the local proxy server is running inside the current long-lived CLI or TUI process.
- `proxy serve` remains a foreground process. Any takeover-capable flow must either run inside that foreground process or start the same in-process server before rewriting live config.
- There are no one-shot CLI takeover or restore commands in this phase. CLI takeover is only exposed through long-running `proxy serve` session flags.
- On normal shutdown, the service restores all active takeovers before the process exits.
- On the next launch, sta...

## State Model

- Runtime truth comes from `ProxyService` and `ProxyStatus`: whether the proxy server is running, which app takeovers are active, and which listen address is currently valid.
- Persistent per-app truth comes from the existing per-app proxy config row. The app-level `enabled` flag is the source of truth for manual takeover intent in this phase.
- `proxy_enabled` stays as a thin global summary flag for simple UX and compatibility. It must not become an independent routing switch.
- `auto_failover_enabled` remains inert compatibility data.
- Any restore marker such as `live_takeover_active` is re...

## Checkpoint Strategy

- Checkpoint 0: commit the current Phase B proxy baseline before new behavior work starts.
- Checkpoint 1: align the runtime pipeline with upstream module boundaries, while keeping single-provider routing.
- Checkpoint 2: add manual per-app takeover and restore lifecycle, without failover.
- Checkpoint 3: expose the smallest useful CLI/TUI takeover controls....

## Checkpoint 0: Freeze the Current Phase B Baseline

**Files:**
- Modify: current proxy runtime and tests already in the worktree
- Add: `docs/plans/2026-03-10-proxy-phase-c-manual-takeover.md`

**Step 1: Verify the current baseline**
- Run `cargo fmt`.
- Run `cargo test --test proxy_claude_streaming -- --nocapture`.
- Run `cargo test --test proxy_multi_app_passthrough -- --nocapture`.
- Run `cargo test proxy_ -- --nocapture`.
- Run `cargo test provider_model_roundtrip_preserves_phase2_fields -- --nocapture`.

**Step 2: Commit the baseline**
```bash
git add docs/plans/2026-03-10-proxy-phase-c-manual-takeover.md src-tauri
git commit -m "feat(prox...

## Deferred After This Plan

- Automatic failover and failover switch management
- Failover queue editing and queue-aware provider routing
- Usage dashboards, request log UI, and pricing UI
- Tray integration or GUI event synchronization
- TUI editing for low-level timeout or retry policy values...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
