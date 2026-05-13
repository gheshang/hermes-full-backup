---
title: Orchestrator Role
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, inference]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Orchestrator Role (delegate_task)

v0.11.0新增，`delegate_task`的子agent现在有显式的`orchestrator`角色，可以再spawn自己的worker。

## 关键参数

- `max_spawn_depth` — 控制嵌套深度（默认flat=1层）
- 跨agent文件状态协调 — 并发子agent通过文件协调层避免互相踩文件

## 使用场景

当任务需要分层调度时：顶层orchestrator拆分任务，worker执行具体工作，orchestrator汇总结果。

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-v0.11.0]] — 引入此特性的版本
