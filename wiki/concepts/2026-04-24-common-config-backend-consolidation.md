---
title: Common Config Backend Upstream Alignment Plan
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/2026-04-24-common-config-backend-consolidation.md]
---

# Common Config Backend Upstream Alignment Plan

源文档：[Common Config Backend Upstream Alignment Plan](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-04-24-common-config-backend-consolidation.md)

# Common Config Backend Upstream Alignment Plan

## Goal

Align the backend common-config implementation with the upstream backend model
as much as this CLI/TUI repository can safely support.

When this repository and upstream disagree, the backend should learn from and,
where suitable, reuse the upstream implementation. The TUI may keep a different
product shape, but it must not force backend common-config semantics away from
the upstream model.

The practical goal is to make these paths agree:

- provider storage snapshots
- live config writes
- switch backfill
- proxy/takeover live backups
- config import/restore live sync
- CLI export
- TUI provi...

## Upstream Source Of Truth

Use these upstream paths as the primary implementation reference:

- `.upstream/cc-switch/src-tauri/src/services/provider/live.rs`
- `.upstream/cc-switch/src-tauri/src/services/provider/mod.rs`
- `.upstream/cc-switch/src-tauri/src/provider.rs`
- `.upstream/cc-switch/src-tauri/src/services/proxy.rs`

The most important upstream functions to mirror or adapt are:

- `provider_uses_common_config`
- `settings_contain_common_config`
- `apply_common_config_to_settings`
- `remove_common_config_from_settings`
- `build_effective_settings_with_common_config`
- `write_live_with_common_config`
- `strip_com...

## Review Resolution

A review found that the previous plan mixed two incompatible goals:

- preserving the current repository's `commonConfigEnabled` default behavior
- claiming Phase 4 upstream alignment

This revision chooses upstream alignment for backend semantics.

The revised plan therefore treats these items as blocking requirements:

- missing `commonConfigEnabled` must follow upstream subset detection, not
  unconditional enablement
- Codex runtime/provider-local TOML tables must be protected beyond
  auto-extraction
- JSON and TOML stripping must support upstream subset and array-subset rules
- config im...

## Target Semantics

### Common-config enablement

Adopt the upstream rule:

- if `meta.commonConfigEnabled` is `Some(true)`, apply a non-empty snippet
- if `meta.commonConfigEnabled` is `Some(false)`, do not apply it
- if `meta.commonConfigEnabled` is `None`, apply only when the provider
  snapshot already contains the snippet as a subset
- OpenCode and OpenClaw do not receive normal common-config live merges

This differs from the current repository behavior, where missing
`commonConfigEnabled` effectively behaves as enabled for Claude, Codex, and
Gemini.

### Legacy migration

For upstream, legacy migration can...

## Repository-Specific Constraints

This repository differs from upstream in product shape and persistence flow.

Important constraints:

- current state uses both DB and in-memory `MultiAppConfig`
- `state.save()` can overwrite DB current provider if stale in-memory
  `manager.current` is written back
- TUI provider forms currently own part of common-config behavior
- front-end layout and workflows may remain CLI/TUI-specific

Backend alignment must therefore be adapted, not copied blindly:

- direct DB writes are acceptable only when later `state.save()` cannot
  overwrite them
- transaction closures that mutate provider snaps...

## Non-Goals

Do not combine this work with:

- hot-switch current-provider cleanup
- removing switch `refresh_snapshot`
- unrelated provider UI redesign
- broad Codex TOML helper rewrites beyond common-config behavior
- changing OpenCode/OpenClaw common-config support

These can be separate follow-ups....

## Target Module Shape

Create a backend common-config module:

- `src-tauri/src/services/provider/common_config.rs`

Prefer function names close to upstream:

- `provider_uses_common_config(app_type, provider, snippet)`
- `settings_contain_common_config(app_type, settings, snippet)`
- `apply_common_config_to_settings(app_type, settings, snippet)`
- `remove_common_config_from_settings(app_type, settings, snippet, mode)`
- `build_effective_settings_with_common_config(state/db, app_type, provider)`
- `normalize_provider_common_config_for_storage(state/db, app_type, provider)`
- `strip_common_config_from_live_settings(s...

## Implementation Tasks

### Task 1: Add Tests For Upstream Semantics

Add tests before changing behavior.

Required cases:

- explicit `commonConfigEnabled=true` applies a non-empty snippet
- explicit `commonConfigEnabled=false` does not apply even if settings contain
  the snippet
- missing `commonConfigEnabled` applies only when settings contain the snippet
  as a subset
- missing `commonConfigEnabled` does not apply when settings do not contain the
  snippet
- legacy migration marks matching providers as `commonConfigEnabled=true`
  and strips the common snapshot fields
- upgrade/startup migration marks old missin...

## Commit Slicing

Recommended commit order:

1. Add tests that document upstream target semantics and current gaps.
2. Port/adapt upstream JSON/TOML common-config helpers.
3. Adopt upstream `provider_uses_common_config` and legacy migration.
4. Add Codex runtime-key guardrails.
5. Replace backend live write, backfill, backup, export, and config sync call
   sites.
6. Add minimal TUI compatibility changes so forms do not defeat backend
   semantics.
7. Run the full verification matrix and fix regressions.

Do not mix this with unrelated hot-switch or refresh-snapshot cleanup....

## Acceptance Criteria

This phase is complete when:

- backend common-config enablement follows upstream explicit/legacy-subset
  semantics
- upstream JSON and TOML subset/array behavior is ported or faithfully adapted
- provider storage normalization, switch backfill, live writes, proxy backups,
  and config restore live sync share the same effective-settings logic
- Codex runtime provider-local tables are protected from common-config stripping
  and extraction
- existing legacy providers that used common config continue working after
  migration
- TUI forms no longer force missing `commonConfigEnabled` into explic...

## Recommended Next Step

Start with Task 1 and Task 2.

The first implementation commit should make the upstream target behavior
executable in tests and port the pure helper algorithms. Avoid changing TUI
behavior or transaction/current-provider behavior until the helper behavior is
locked down....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
