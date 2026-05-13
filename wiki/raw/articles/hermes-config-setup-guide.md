---
source_url: https://github.com/hermes-agent/skills/tree/main/devops/hermes-config-setup
ingested: 2026-04-24
sha256: embedded-from-skill
---

# Hermes Agent 配置引导脚本

## 核心配置项

### 1. 副驾模型（auxiliary）— 省 token 的关键
- 重任务(vision/web_extract/flush_memories)用稍强模型
- 轻任务(compression/session_search/approval/skills_hub/mcp)用便宜快模型

### 2. 搜索后端
- tavily（月1000次免费）或 duckduckgo（零成本）
- 建议配duckduckgo兜底

### 3. 记忆系统
- memory_enabled/user_profile_enabled 默认true
- memory_char_limit=2200, user_char_limit=1375
- nudge_interval=10, flush_min_turns=6

### 4. Profile分身
- hermes profile create/use/-p

### 5. Skill自主进化
- creation_nudge_interval=15

### 6. 子Agent并发
- delegation.max_concurrent_children=2-3

### 7. Cron定时任务
- 前置条件：gateway必须跑

### 8. Token监控与压缩
- tokscale/hermes-dashboard/hermes dashboard
- RTK (Rust Token Killer)

## 编写脚本的安全坑（高危）

1. shell=True + 用户输入拼接 = 命令注入 — 必须用列表传参
2. API Key不能明文写config.yaml — 必须写.env
3. .env文件必须设0600权限
4. .env写入要去重 — 已有key精确替换
5. 后台进程不能用shell的& — 用Popen+start_new_session=True
6. 用户输入拼入示例命令必须shlex.quote()转义

## 逻辑坑（中危）
7. split("=")会切碎含=的值 — 用split("=",1)
8. api_key_env默认值不能用空dict{} — 用None
9. 整数参数必须有边界校验
10. Profile名必须校验
11. 死变量必须删
