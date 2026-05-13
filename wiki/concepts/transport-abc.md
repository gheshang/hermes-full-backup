---
title: Transport ABC
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework, inference]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Transport ABC

v0.11.0新增，将格式转换和HTTP传输从`run_agent.py`抽出为`agent/transports/`可插拔层。

## 四种Transport

| Transport | 用途 |
|-----------|------|
| AnthropicTransport | Anthropic Messages API |
| ChatCompletionsTransport | 默认OpenAI兼容路径 |
| ResponsesApiTransport | OpenAI Responses API + Codex |
| BedrockTransport | AWS Bedrock Converse API |

每个Transport独立拥有自己的格式转换和API shape。

## 意义

之前所有provider的格式处理都混在run_agent.py里。现在每个provider的逻辑自包含，新增provider只需实现Transport ABC，不需要动核心代码。

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-v0.11.0]] — 引入此概念的版本
