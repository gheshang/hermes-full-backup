---
title: Feishu Improvements
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [feishu, agent]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Feishu Adapter Improvements (v0.11.0)

飞书适配器的3项重要更新。

## 新功能

1. **智能回复文档评论** — 3级访问控制，agent可在飞书文档评论中智能回复
2. **处理状态reactions** — 用户消息上显示处理中状态（emoji reaction），让用户知道agent正在工作
3. **@mention上下文保留** — 保留@提及的上下文给agent消费，不再丢失引用信息

## 之前的问题

- 文档评论无法回复
- 用户不知道agent是否在处理
- @mention信息在传递中丢失

## 关联

- [[hermes-agent]] — 框架本体
- [[wecom-setup]] — 同期WeCom改进
