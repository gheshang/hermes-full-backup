---
title: Proxy B Single-Provider UX Implementation Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-03-09-proxy-b-single-provider-ux.md]
---

# Proxy B Single-Provider UX Implementation Plan

源文档：[Proxy B Single-Provider UX Implementation Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-09-proxy-b-single-provider-ux.md)

# Proxy B Single-Provider UX Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Keep the local proxy and issue #49 transform path, but make it easy to configure from the maintained TUI without adding failover.

**Architecture:** Reuse the current Phase B proxy core and add only the smallest user-facing pieces: a Claude `apiFormat` toggle in the TUI provider form, clearer proxy setup guidance, and more obvious issue #49 setup hints. Keep runtime behavior single-provider and DB-driven, with no provider router or automatic failover lifecycle.

**Tech Stack:** Rust, tokio, ratatui, serde_json, existing TUI form/app layers, proxy core modules.

---

### Task 1: Add failing Claude apiFormat form tests

**File

## Status Snapshot (2026-03-09)

### Implemented

- Claude provider form now exposes `apiFormat`, with `anthropic` and `openai_chat` options, and persists the canonical upstream-style `meta.apiFormat` value.
- Claude provider edit/detail views now show the chosen API format, so the issue #49 path is visible from the maintained TUI.
- `Config -> Local Proxy` now includes a manual Claude hookup guide: run `cc-switch proxy serve`, point `ANTHROPIC_BASE_URL` at the local proxy, and use a placeholder auth token.
- `cc-switch proxy show` now mirrors that same manual setup path, so the foreground CLI and TUI tell the same story.

##...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
