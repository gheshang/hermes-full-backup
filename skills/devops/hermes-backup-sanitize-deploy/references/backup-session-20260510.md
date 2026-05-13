# 备份会话记录: 2026-05-10

## 执行概要

| 项目 | 值 |
|------|-----|
| 仓库 | `gheshang/hermes-backup` |
| 提交 | `40fe9cb` |
| 变更 | 792 文件，+121,362 / -3,463 行 |
| 大小 | ~18.5 MB |

## 排除清单（最终确认）

```
.env, .env.*, auth.json, auth.lock
sessions/, logs/, hindsight/, checkpoints/
state.db*, kanban.db, response_store.db
feishu_seen_message_ids.json, gateway_state.json
gateway.pid, gateway.lock, processes.json
interrupt_debug.log, models_dev_cache.json
.skills_prompt_snapshot.json, SOUL.md.bak
config.yaml.bak, __pycache__/, node/, cache/
image_cache/, images/, audio_cache/, sandboxes/
.herms_history, channel_directory.json
backups/, state-snapshots/, plans/, weixin/
pairing/, hooks/, bin/, hermes-agent/
cron/output/, cron/.tick.lock
```

## 关键操作

1. **已跟踪敏感文件移除**：`.env`、`cron/output/*`（14个文件）、`cron/.tick.lock`、`hindsight/config.json` 均已被 git 跟踪，使用 `git rm --cached` 从跟踪中移除。
2. **`.gitignore` 更新**：添加完整排除列表，确保后续 `git add -A` 不会误传。
3. **增量备份**：clone 已有仓库 → 替换内容 → `git add -A` → commit → push，未使用 force push。
4. **SSH 认证**：`gh` CLI 未安装，使用 SSH key 认证 (`ssh -T git@github.com` 返回 `Hi gheshang!`) 直接 push。

## 备份内容

- `config.yaml` + `config-backups/` + `config.yaml.bak.homechannel`
- `skills/`（全部自定义技能，含新安装的 comfyui、gpt-image-2、html-ppt 等）
- `memories/`（USER.md + MEMORY.md）
- `profiles/`、`wiki/`、`cron/jobs.json`
- `SOUL.md`、`hermes_setup_all.py`、`skills-inventory.md`
- 独立项目：`agency-agents-zh/`、`andrej-karpathy-skills/`、`superpowers/`、`tencentyun-snake-up/`
