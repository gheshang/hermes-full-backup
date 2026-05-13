---
title: Browser CDP
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [browser, agent, anti-bot]
sources: [raw/articles/hermes-v0.11.0-release-notes.md]
---

# Browser CDP Passthrough (v0.11.0)

新增`browser_cdp`工具，提供原始DevTools Protocol透传能力。

## 用途

- 直接发送CDP命令给浏览器
- 突破内置browser工具的限制
- 实现更底层的浏览器控制（网络拦截、DOM修改等）

## 关联

- [[hermes-agent]] — 框架本体
- [[shell-hooks]] — 同期新增的底层能力
