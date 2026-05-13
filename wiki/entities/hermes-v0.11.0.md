---
title: Hermes Agent v0.11.0
created: 2026-04-24
updated: 2026-04-24
type: entity
tags: [agent, framework, timeline]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Hermes Agent v0.11.0 (v2026.4.23)

"The Interface Release" — 1,556 commits · 761 merged PRs · 1,314 files changed sincev0.9.0。

## 关键变更

### 新功能
- **Ink TUI** — `hermes --tui` 全新React/Ink交互CLI，~310 commits
- **Transport ABC** — 格式转换和HTTP传输抽出为可插拔层，见[[transport-abc]]
- **5个新推理路径** — NVIDIA NIM / Arcee AI / Step Plan / Gemini CLI OAuth / Vercel ai-gateway
- **GPT-5.5** — Codex OAuth + 实时模型发现
- **QQBot** — 第17个消息平台
- **[[orchestrator-role]]** — 子agent可嵌套spawn，可配置max_spawn_depth
- **[[shell-hooks]]** — 生命周期钩子脚本
- **[[browser-cdp]]** — DevTools Protocol原始透传
- **`/steer`** — 中途注入agent指令，不中断当前轮次

### 与飞书/微信用户相关
- [[feishu-improvements]] — 智能文档评论回复、@mention上下文保留、处理状态reactions
- [[wecom-setup]] — 企业微信QR-scan bot创建+设置向导
- 压缩摘要尊重对话语言
- [[compression-anti-thrashing]] — 智能折叠/去重/防抖

### 稳定性修复
- 压缩耗尽无限循环 → 自动重置session
- 弱模型空响应后过早退出循环 → 修复
- gateway重启后自动恢复中断的agent工作
- 活动心跳防止虚假gateway超时
- `/stop`不再重置session

## 零Breaking Changes

此版本无破坏性变更，无需迁移。
