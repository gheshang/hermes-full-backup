---
title: Hermes Agent
created: 2026-04-24
updated: 2026-04-24
type: entity
tags: [agent, framework, open-source, llm]
sources: [raw/articles/hermes-v0.11.0-release-notes.md, raw/articles/hermes-agents-md-developer-guide.md]
---

# Hermes Agent

开源AI Agent框架，由Nous Research开发，MIT协议。核心特性：自我改进循环、三层记忆、多平台网关、skill系统。

## 当前版本

v0.11.0 (2026.4.23) — "The Interface Release"

## 核心架构

- **AIAgent** (`run_agent.py`, ~12k LOC) — 核心对话循环，同步执行，含中断检查/预算追踪/grace call
- **Transport层** (`agent/transports/`) — v0.11新增，4种传输：Anthropic/ChatCompletions/ResponsesApi/Bedrock
- **CLI** (`cli.py`, ~11k LOC) + **TUI** (`ui-tui/`, Ink/React)
- **Gateway** (`gateway/platforms/`) — 17个消息平台适配器
- **Plugin系统** (`plugins/`) — 内存/context引擎/image-gen/清理等

## 关键能力

| 能力 | 说明 |
|------|------|
| Skill系统 | `skills/`(内置) + `optional-skills/`(可选)，SKILL.md格式 |
| 三层记忆 | session/memory/user，支持多种memory provider |
| 自我改进 | 每15次任务触发 do→learn→improve 循环 |
| 多平台 | Telegram/Discord/Slack/微信/飞书/企业微信/QQBot等17个 |
| 子agent | [[orchestrator-role]] + 可配置spawn深度 |
| 压缩器 | [[compression-anti-thrashing]]，上下文压缩防无限循环 |
| Cron | 支持[[cron-toolsets]]按job限制工具集 |
| 浏览器 | [[browser-cdp]] DevTools Protocol透传 |

## 配置

- `~/.hermes/config.yaml` — 设置
- `~/.hermes/.env` — API密钥（仅密钥，非设置）
- `~/.hermes/logs/` — agent.log / errors.log / gateway.log

## 版本线

| 版本 | 日期 | 代号 |
|------|------|------|
| v0.8.0 | 2026.4.8 | — |
| v0.9.0 | 2026.4.13 | Everywhere |
| v0.10.0 | 2026.4.16 | Tool Gateway |
| v0.11.0 | 2026.4.23 | Interface |
