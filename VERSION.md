# Hermes Agent 备份信息

- **备份时间**: 2026-07-07 09:20:22 CST
- **服务器**: HKTJser0417215710
- **操作系统**: Linux HKTJser0417215710 6.8.0-124-generic #124-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 13:00:45 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
- **Hermes 提交**: 1c4cc00f7 fix(moa): user_turn fanout — synthetic advisory marker must not count as a user turn (#57598)
- **Hermes 标签**: v2026.6.19-2090-g1c4cc00f7
- **Skills 数量**: 177
- **cron 任务数**: 6
- **配置文件**: config.yaml

## 备份内容

| 目录/文件 | 说明 |
|-----------|------|
| config/ | Hermes Agent 配置 |
| skills/ | 全部 177 个 Skill 文件 |
| memories/ | 持久记忆（USER.md + MEMORY.md） |
| cron/ | 定时任务配置 |
| pairing/ | 飞书/微信配对授权 |
| checkpoints/ | 文件系统检查点 |
| plans/ | 历史规划记录 |
| kanban.db | Kanban 看板数据 |
| .env | API Key 占位模板（需手动填入） |

## 恢复指引

1. 安装 Hermes Agent
2. 将 skills/ 复制到 ~/.hermes/skills/
3. 将 config.yaml 复制到 ~/.hermes/config.yaml
4. 复制 .env 并填入真实 API Key
5. 复制 memories/ 到 ~/.hermes/memories/
6. 如有 cron 任务，复制 cron/ 到 ~/.hermes/cron/
