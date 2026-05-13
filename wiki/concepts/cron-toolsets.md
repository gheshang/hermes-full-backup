---
title: Cron Per-Job Toolsets
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Cron Per-Job enabled_toolsets (v0.11.0)

Cron任务现在支持按job设置`enabled_toolsets`，限制每个job可用的工具集。

## 意义

- **省token** — 只加载job需要的工具，减少system prompt开销
- **省成本** — 减少每轮的input token数
- **安全** — 限制cron job的能力范围

## 新增: wakeAgent gate

Cron的script可以先检查条件，决定是否需要唤醒agent。如果script返回结果不需要agent处理，直接跳过，零LLM调用。

## 关联

- [[hermes-agent]] — 框架本体
- [[shell-hooks]] — 另一种降低开销的方式
