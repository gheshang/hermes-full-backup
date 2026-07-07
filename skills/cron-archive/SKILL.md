---
name: cron-archive
description: 定时任务统一存档管理 — 涵盖 Hermes Cron 和系统 crontab，含索引、汇总、清理。
version: 1.0.0
author: 上河一号
metadata:
  hermes:
    tags: [cron, archive, backup, automation]
    priority: normal
---

# Cron Archive Manager

管理所有定时任务的本地存档，包括 Hermes Cron 和系统 crontab。

## 目录结构

```
~/.hermes/cron/archive/
├── index.json              # 统一索引
├── hermes -> ../output     # 软链接到 Hermes cron 输出
├── system -> ../lian-zhou-jobs  # 软链接到系统 crontab 输出
├── daily_summary.sh        # 每日汇总脚本
└── monthly_cleanup.sh      # 月度清理脚本（保留90天）
```

## 参考文档

- `references/cron-deliver-config.md` — Cron deliver 配置指南（Hermes Cron 原生交付 + 脚本内嵌推送）
- `references/cron-script-patterns.md` — 脚本直跑模式（no_agent + script）详解
- `references/news-briefing-pattern.md` — LLM 驱动定时新闻/研究简报模式（多源采集 → 中文编译 → 飞书推送）
- `references/lianzhou-jobs-troubleshooting.md` — lian-zhou-jobs 故障排查（bs4 依赖、飞书推送、路径错误）

## 常用命令

### 查看今日所有任务输出
```bash
bash ~/.hermes/cron/archive/daily_summary.sh
```

### 查看指定日期
```bash
bash ~/.hermes/cron/archive/daily_summary.sh 2026-05-14
```

### 查看特定任务历史
```bash
ls ~/.hermes/cron/archive/hermes/1c98c5dc724d/
```

### 月度清理（保留最近 90 天）
```bash
bash ~/.hermes/cron/archive/monthly_cleanup.sh
```

## Hermes Cron 使用脚本

Hermes cron **完全可以用脚本**，有两种模式：

### 模式1: no_agent + script（纯脚本执行）
```python
cronjob(action='create',
    script='/path/to/script.sh',
    no_agent=True,
    schedule='0 8 * * *'
)
```
- 脚本 stdout 原样输出，不走 LLM
- 无 token 消耗，适合监控/数据收集
- stdout 为空时 silent，非空时送达
- 参考：`references/cron-script-patterns.md`

### 模式2: prompt + skills（LLM 驱动）
```python
cronjob(action='create',
    prompt='执行每日备份并生成报告',
    skills=['daily-self-audit'],
    schedule='30 2 * * *'
)
```
- LLM 解析 prompt，调用 skills
- 适合需要推理、总结、报告的任务

### 模式3: script + prompt（混合模式 — 数据注入 + LLM 决策）

```python
cronjob(action='create',
    script='check-yesterday-activity.py',   # 脚本 stdout 注入 context
    prompt='检查上下文中是否 INACTIVE，是则输出 [SILENT] 跳过',
    schedule='30 2 * * *'
)
```
- 脚本运行 → stdout 以 `[Script Output]` 形式注入 agent prompt 上下文
- LLM 读取脚本输出 → 根据内容决定是否执行主逻辑
- 适合：**前置检查/守卫（guard）模式** — 条件满足才执行 LLM 任务
- 零额外 token 消耗做前置条件判断（脚本纯跑数据，不消耗推理 tokens）
- 参考示例：`daily-self-audit` 的活动前置检查（5 个 cron 均挂载此模式）

⚠️ **脚本路径约定**：`script` 参数必须是文件名（相对 `~/.hermes/scripts/`），不支持绝对路径。传绝对路径或 `~/` 路径会报错。

### 三种模式对比

| 维度 | no_agent + script | prompt + skills | script + prompt (混合) |
|------|------------------|----------------|----------------------|
| 执行主体 | 脚本直接运行 | LLM 解析后执行 | 脚本收集数据 → LLM 决策 |
| Token 消耗 | 无 | 有 | 仅条件判断有，不满足则跳过 |
| 输出格式 | 脚本 stdout 原样 | LLM 生成的报告 | LLM 生成或 [SILENT] 跳过 |
| 适用场景 | 监控、数据收集、确定性任务 | 需要推理、总结、报告 | 有前置条件的 LLM 任务（守卫模式） |
| 典型示例 | uv-cache-guard.sh | daily-self-audit 审计链 | 活动前置检查 → 跳过自审 |

## 飞书推送状态

| 任务 | 来源 | 飞书推送 | 说明 |
|------|------|---------|------|
| 自审-备份快照 | Hermes Cron | ✅ | `deliver: feishu` |
| 自审-缓存清理 | Hermes Cron | ✅ | `deliver: feishu` |
| 自审-Cron健康检查 | Hermes Cron | ✅ | `deliver: feishu` |
| 自审-Memory检查 | Hermes Cron | ✅ | `deliver: feishu` |
| 自审-Skills+Config检查 | Hermes Cron | ✅ | `deliver: feishu` |
| weekly-cache-cleanup | Hermes Cron | ✅ | 已改为 `deliver: feishu` |
| lian-zhou-jobs | 系统 crontab | ✅ | 脚本内嵌飞书推送，每日 08:00 |

**所有定时任务结果均已推送到飞书。**

## 存档策略

| 类型 | 保留期限 | 清理方式 |
|------|---------|---------|
| Hermes cron output | 90 天 | monthly_cleanup.sh |
| lian-zhou-jobs | 90 天 | monthly_cleanup.sh |
| index.json | 永久 | 手动更新 |

## 本次会话发现（2026-05-15）

### 统一存档管理

创建 `~/.hermes/cron/archive/` 作为统一存档管理层：
- `hermes/` → 软链接到 `output/`（Hermes cron 输出）
- `system/` → 软链接到 `lian-zhou-jobs/`（系统 crontab 输出）
- `index.json` → 统一索引，涵盖两类任务
- `daily_summary.sh` → 每日汇总脚本
- `monthly_cleanup.sh` → 月度清理脚本（保留90天）

### 软链接 vs 复制

使用软链接而非复制：
- 不占用额外磁盘空间
- 源文件更新自动可见
- 清理时只需删源文件，软链接自动失效

### Hermes Cron vs 系统 crontab 区别

| 维度 | Hermes Cron | 系统 crontab |
|------|------------|-------------|
| 运行时 | LLM Agent（hermes CLI） | 系统 shell |
| 执行内容 | Prompt + Skills（LLM 驱动） | 脚本/命令（直接执行） |
| 结果交付 | 可推送到飞书/微信/本地 | 仅 stdout → 日志文件 |
| 上下文 | 有 Agent 会话上下文 | 无上下文，纯脚本 |
| 管理方式 | `hermes cron` 命令 | `crontab -e` |

### 脚本推送飞书模式

lian-zhou-jobs 验证了**脚本内嵌飞书推送**的可行性：
- Python 脚本直接调用飞书 Bot API（tenant_access_token + 消息发送）
- 不依赖 Hermes gateway 或 `hermes send_message`（该命令不存在）
- 凭证从 `~/.hermes/.env` 读取
- 参考：`references/lianzhou-jobs-troubleshooting.md`