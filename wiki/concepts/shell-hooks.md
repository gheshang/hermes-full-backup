---
title: Shell Hooks
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework, deploy]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Shell Hooks (v0.11.0)

将任意shell脚本绑定为Hermes生命周期钩子，无需写Python plugin。

## 支持的钩子点

- `pre_tool_call` / `post_tool_call`
- `on_session_start`
- 其他lifecycle事件

## 与Plugin的区别

Plugin需要Python代码；Shell Hooks只需一个脚本文件，降低定制门槛。

## 关联

- [[hermes-agent]] — 框架本体
- [[browser-cdp]] — 同期新增的底层能力
