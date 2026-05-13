---
title: Plugin Surface Expansion
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Plugin Surface Expansion (v0.11.0)

v0.11.0大幅扩展了Plugin能力面。

## 新增能力

| 能力 | 说明 |
|------|------|
| `register_command()` | Plugin注册slash命令 |
| `dispatch_tool()` | Plugin直接调用工具 |
| `pre_tool_call` veto | Plugin阻止工具执行 |
| `transform_tool_result` | Plugin改写工具结果 |
| `transform_terminal_output` | Plugin改写终端输出 |
| image_gen backend | Plugin提供图片生成后端 |
| Dashboard tabs | Plugin添加自定义dashboard标签页 |

## 附带

- 内置disk-cleanup plugin（默认opt-in）
- OpenAI Codex OAuth image_gen plugin (gpt-image-2)
- 命名空间skill注册 — plugin bundle可带整组skill

## 关联

- [[hermes-agent]] — 框架本体
- [[shell-hooks]] — 另一种hook方式
- [[cron-toolsets]] — 工具限制机制
