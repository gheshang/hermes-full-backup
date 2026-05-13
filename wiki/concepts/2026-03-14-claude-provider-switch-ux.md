---
title: Claude Provider Switch UX Implementation Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-03-14-claude-provider-switch-ux.md]
---

# Claude Provider Switch UX Implementation Plan

源文档：[Claude Provider Switch UX Implementation Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-14-claude-provider-switch-ux.md)

# Claude Provider Switch UX Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a first-use protection dialog before overwriting an existing Claude `settings.json`, and show a one-time post-switch tip about shared common config after the first real Claude provider switch.

**Architecture:** Keep the existing provider list key flow unchanged and intercept the behavior in TUI runtime actions. Add one new three-choice centered overlay for the pre-switch protection, and one reusable close-only notice overlay for the post-switch hint. Persist the one-time hint state in `AppSettings` so it survives restarts.

**Tech Stack:** Rust, ratatui TUI overlays, existing `ProviderService`, existing `AppSettings` per

## Execution Status

- 2026-03-18: Merge conflict resolution preserved the Task 1-4 Claude provider switch UX behavior while keeping OpenClaw support in the provider flows.
- Verified passing during merge resolution with `cargo fmt`, `cargo test cli::tui::runtime_actions::providers --lib`, `cargo test cli::tui::runtime_actions::editor --lib`, `cargo test cli::tui::app::tests --lib`, and `cargo test --test provider_service`.
- Broader verification completed on 2026-03-18 with `cargo test`; the full Rust test suite passed after fixing the Codex stale-takeover current-provider restore path....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
