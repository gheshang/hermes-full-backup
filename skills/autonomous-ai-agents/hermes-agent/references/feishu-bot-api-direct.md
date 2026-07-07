# 飞书 Bot API 直接推送模式

## 背景

Hermes 的 `hermes send_message` 命令不存在。`hermes` CLI 的子命令列表中只有 `chat, model, fallback, gateway, setup, whatsapp, slack, login, logout, auth, status, cron, webhook, kanban, hooks, doctor, dump, debug, backup, checkpoints, import, config, pairing, skills, plugins, curator, memory, tools, mcp, sessions, insights, claw, version, update, uninstall, acp, profile, completion, dashboard, logs`。

**结论**：脚本中需要发送飞书消息时，不能依赖 `hermes send_message`，必须直接用飞书 Bot API。

## 实现模式

### 1. 从 .env 读取飞书凭证

```python
import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
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
```

### 2. 获取 tenant_access_token

```python
import requests

token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
token_resp = requests.post(
    token_url,
    json={"app_id": app_id, "app_secret": app_secret},
    headers={"Content-Type": "application/json"},
    timeout=10,
)
token_data = token_resp.json()
if token_data.get("code") != 0:
    # 处理错误
    return
access_token = token_data["tenant_access_token"]
```

### 3. 发送消息

```python
msg_url = "https://open.feishu.cn/open-apis/im/v1/messages"
msg_resp = requests.post(
    msg_url,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    },
    json={
        "receive_id": "oc_xxxxxxxxxxxxxxxxxxxx",  # 群组或用户 open_id
        "receive_id_type": "open_chat_id",  # 或 "open_id" 用于 DM
        "content_type": "text",
        "content": json.dumps({"text": "消息内容"}, ensure_ascii=False),
    },
    timeout=10,
)
msg_data = msg_resp.json()
if msg_data.get("code") != 0:
    # 处理发送失败
    pass
```

## 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `receive_id_type` | `open_chat_id` | 发送到群组 |
| `receive_id_type` | `open_id` | 发送给用户 DM |
| `content_type` | `text` | 纯文本消息 |
| `content_type` | `post` | 富文本消息（支持标题、高亮等） |
| `content_type` | `interactive` | 交互式卡片 |

## 注意事项

1. **App 权限**：飞书开放平台中，App 需要申请 `im:message` 和 `im:message.readonly` 权限，且需管理员审核通过。
2. **群组添加**：App 必须被添加到目标群组，否则发送会失败。
3. **Token 缓存**：`tenant_access_token` 有效期 2 小时，频繁调用时应缓存，不要每次请求都重新获取。
4. **频率限制**：飞书 API 有调用频率限制，大批量发送时需控制速率。
5. **凭证安全**：FEISHU_APP_SECRET 是敏感信息，脚本中读取 .env 时注意权限（chmod 600）。

## 适用场景

- Cron 脚本需要主动推送通知到飞书
- 独立 Python 脚本需要飞书通知
- Hermes gateway 不可用时的备选方案
