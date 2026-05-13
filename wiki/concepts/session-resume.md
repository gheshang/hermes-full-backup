---
title: Session Resume
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Session Resume (v0.11.0)

Gateway重启后自动恢复中断的agent工作。

## 机制

- Activity heartbeats — 防止虚假gateway不活跃超时
- 重启后检测中断的session → 自动继续
- 修复了反复重启后卡在resume循环的bug

## 关联

- [[hermes-agent]] — 框架本体
- [[compression-anti-thrashing]] — 另一个稳定性修复
