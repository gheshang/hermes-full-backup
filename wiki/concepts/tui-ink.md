---
title: TUI Ink
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Ink-based TUI (v0.11.0)

`hermes --tui` 全新React/Ink重写的交互式CLI，~310 commits。

## 特性

- Sticky composer — 输入时冻结，滚动时不丢失
- OSC-52剪贴板 — SSH下也能复制
- 稳定picker键
- 状态栏：每轮计时器 + git分支
- `/clear` 确认
- 浅色主题
- 子agent spawn可观测overlay
- Python JSON-RPC后端 (`tui_gateway/`)

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-v0.11.0]] — 引入此功能的版本
