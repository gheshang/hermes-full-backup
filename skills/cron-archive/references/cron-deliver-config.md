# Cron Deliver 配置指南

## 两种交付方式

### 1. Hermes Cron 原生交付（推荐）

通过 `cronjob` 工具的 `deliver` 参数控制：

```python
cronjob(action='create',
    prompt='执行每日备份快照',
    schedule='30 2 * * *',
    deliver='feishu'  # 或 'local', 'all'
)
```

**deliver 选项：**
| 值 | 说明 |
|----|------|
| `feishu` | 推送到飞书（默认，如果 cron 创建时来自飞书会话） |
| `local` | 仅本地存档，不推送 |
| `all` | 推送到所有连接的平台 |
| `platform:chat_id` | 指定特定聊天 |

**修改现有任务的 deliver：**

Hermes cron 的配置存储在 `~/.hermes/cron/jobs.json` 中。修改步骤：

```python
import json

jobs_path = '/home/hangskf/.hermes/cron/jobs.json'
with open(jobs_path) as f:
    data = json.load(f)

for job in data['jobs']:
    if job['id'] == '<job_id>':
        job['deliver'] = 'feishu'  # 修改为目标值

with open(jobs_path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**验证：** `hermes cron list` 查看 `Deliver` 字段

### 2. 脚本内嵌推送（系统 crontab）

系统 crontab 任务无法使用 Hermes Cron 的 `deliver` 参数，需要在脚本内嵌推送逻辑。

**lian-zhou-jobs 示例：**

```python
def send_feishu(jobs: list[dict], today: str, total: int):
    """通过飞书 Bot API 发送到飞书群组。"""
    # 从 .env 读取飞书凭证
    env_file = BASE_DIR / ".env"
    app_id = ""
    app_secret = ""
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("FEISHU_APP_ID="):
                app_id = line.split("=", 1)[1].strip()
            elif line.startswith("FEISHU_APP_SECRET="):
                app_secret = line.split("=", 1)[1].strip()

    if not app_id or not app_secret:
        log.error("飞书凭证未配置，跳过推送")
        return

    # 1. 获取 tenant_access_token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_resp = requests.post(token_url, json={"app_id": app_id, "app_secret": app_secret})
    access_token = token_resp.json()["tenant_access_token"]

    # 2. 发送消息
    msg_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    msg_resp = requests.post(msg_url, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }, json={
        "receive_id": FEISHU_TARGET,
        "receive_id_type": "open_chat_id",
        "content_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    })
```

**关键配置：**
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET`：在 `~/.hermes/.env` 中配置
- `FEISHU_TARGET`：目标 chat_id（open_chat_id 格式）
- 需要安装 `requests` 库：`pip3 install requests`

## 统一存档管理

所有 cron 任务结果统一存档在 `~/.hermes/cron/archive/`：

```
archive/
├── index.json              # 统一索引
├── hermes -> ../output     # 软链接到 Hermes cron 输出
├── system -> ../lian-zhou-jobs  # 软链接到系统 crontab 输出
├── daily_summary.sh        # 每日汇总
└── monthly_cleanup.sh      # 90 天自动清理
```

**每日汇总：**
```bash
bash ~/.hermes/cron/archive/daily_summary.sh              # 今日
bash ~/.hermes/cron/archive/daily_summary.sh 2026-05-14   # 指定日期
```
