---
title: Proxy B Multi-App Skeleton Implementation Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-03-09-proxy-b-multiapp-skeleton.md]
---

# Proxy B Multi-App Skeleton Implementation Plan

源文档：[Proxy B Multi-App Skeleton Implementation Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-09-proxy-b-multiapp-skeleton.md)

# Proxy B Multi-App Skeleton Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an upstream-aligned multi-app proxy skeleton to the CLI repo, with Claude usable first, Codex/Gemini routes and service structure present, and no live takeover yet.

**Architecture:** Reuse the upstream proxy split as much as possible: `proxy/*` contains server, handlers, forwarder, providers, and streaming conversion; a thin CLI-facing service layer starts and stops the local server and reads existing DB-backed proxy config. Phase B keeps proxy serving and runtime config aligned with upstream, but deliberately leaves takeover, backup/restore, and crash recovery outside the first implementation.

**Tech Stack:** Rust, to

## Status Snapshot (2026-03-09)

### Implemented in Solution B

- Provider metadata now aligns with upstream `apiFormat`, including `openai_chat` roundtrip support.
- Added a thin CLI-side `ProxyService` that starts/stops the local server and reads DB-backed proxy config without introducing takeover behavior.
- Added upstream-shaped multi-app routes for Claude, Codex, and Gemini.
- Claude supports `apiFormat=openai_chat` request/response conversion and streaming SSE conversion back to Anthropic format.
- Codex supports passthrough for `/v1/chat/completions` and `/v1/responses`.
- Gemini supports passthrough for `/v1beta/*` ro...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
