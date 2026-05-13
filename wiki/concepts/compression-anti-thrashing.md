---
title: Compression Anti-Thrashing
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, inference]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Compressor Anti-Thrashing

v0.11.0对上下文压缩器的重大改进。

## 修复的问题

- **压缩耗尽无限循环** — 压缩失败后反复重试直到耗尽所有token → 现在自动重置session
- **重试计数器不重置** — 压缩后retry计数器残留导致后续请求误判 → 修复
- **压缩摘要语言** — 之前摘要可能用英语而对话是中文 → 现在尊重对话语言

## 改进

- 智能折叠 — 识别重复内容合并
- 去重 — 相似上下文片段合并
- 防抖 — 防止频繁压缩循环
- 压缩模型503/404回退 — 自动降级到主模型

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-v0.11.0]] — 包含此修复的版本
