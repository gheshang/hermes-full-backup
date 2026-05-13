---
title: Hermes Agent 配置引导
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [agent, framework, deploy]
sources: [raw/articles/hermes-config-setup-guide.md]
---

# Hermes Agent 配置引导

交互式脚本配置Hermes Agent的9大功能模块。

## 9大配置项

| # | 模块 | 核心 |
|---|------|------|
| 1 | 副驾模型 | 重任务用强模型，轻任务用便宜模型，省token |
| 2 | 搜索后端 | tavily(月1000次免费)/duckduckgo(零成本) |
| 3 | 记忆系统 | memory_enabled/char_limit/nudge_interval |
| 4 | Profile分身 | 创建/切换/临时切换 |
| 5 | Skill自主进化 | creation_nudge_interval=15 |
| 6 | 子Agent并发 | max_concurrent_children=2-3 |
| 7 | Cron定时 | gateway必须跑 |
| 8 | Token监控 | tokscale/dashboard + RTK压缩 |
| 9 | 生态工具 | 380+/1000+ skill库，Pandoc/Marker |

## 6个安全高危坑

1. **命令注入** — `shell=True`+用户输入拼接=绝对禁止，用列表传参
2. **API Key明文** — 不能写config.yaml，必须写.env
3. **.env权限** — 必须0600，`os.chmod(path, S_IRUSR|S_IWUSR)`
4. **.env去重** — 已有key精确替换，不盲追加
5. **后台进程** — 不用shell的`&`，用`Popen(start_new_session=True)`
6. **用户输入转义** — `shlex.quote()`防命令断裂

## 交互脚本限制

Hermes terminal工具无法运行需要`input()`的脚本（pty模式下EOFError）。用户必须在本地终端手动运行，或直接告诉Hermes配置信息由Hermes后台配置。

## 关联

- [[hermes-agent]] — 被配置的框架
- [[vps-init-script]] — 配置前的VPS初始化
