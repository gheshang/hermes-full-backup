# 飞书 Webhook 消息接收与推送 · 完整代码

## 飞书 Webhook 接收（FastAPI）

```python
from fastapi import FastAPI, Request, HTTPException
import httpx
import os
import json

app = FastAPI()

FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL")
DIFY_API_URL = os.getenv("DIFY_API_URL")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

@app.post("/api/webhook/feishu")
async def feishu_webhook(request: Request):
    """飞书事件回调"""
    body = await request.json()
    
    # 验证飞书签名（生产环境必须）
    # 简化版：生产环境请添加签名验证
    
    if body.get("type") == "url_verification":
        return {"challenge": body.get("challenge")}
    
    # 解析消息
    message = body.get("event", {}).get("message", {})
    content = message.get("content", {})
    text = content.get("text", "").strip()
    
    if not text:
        return {"code": 0}
    
    # 转发到分析服务
    await process_message("feishu", text, message)
    
    return {"code": 0}

async def process_message(source: str, content: str, raw_data: dict):
    """处理消息：转发到Dify分析"""
    payload = {
        "inputs": {},
        "query": content,
        "response_mode": "blocking",
        "user": f"{source}_{raw_data.get('sender', 'unknown')}"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{DIFY_API_URL}/workflows/run",
            headers={"Authorization": f"Bearer {DIFY_API_KEY}"},
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            await send_alert(result)

async def send_alert(analysis_result: dict):
    """发送飞书告警卡片"""
    level = analysis_result.get("data", {}).get("alert_level", "normal")
    
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": f"🚨 {level.upper()} 告警"},
                "template": "red" if level == "high" else "blue"
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": analysis_result.get("data", {}).get("summary", "无摘要")}},
                {"tag": "div", "text": {"tag": "lark_md", "content": "**AI分析结论：**" + analysis_result.get("data", {}).get("conclusion", "无结论")}},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"}, "type": "primary", "url": analysis_result.get("data", {}).get("link", "")}
                ]}
            ]
        }
    }
    
    async with httpx.AsyncClient() as client:
        await client.post(FEISHU_WEBHOOK, json=card)
```

## 飞书 Webhook 发送（含签名验证）

```python
#!/usr/bin/env python3
# coding:utf-8
# 飞书Webhook发送消息（含签名验证）

import base64
import hashlib
import hmac
from datetime import datetime
import requests

WEBHOOK_URL = "你的飞书Webhook地址"
WEBHOOK_SECRET = "***"

def gen_sign(secret, timestamp):
    string_to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), 
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(hmac_code).decode('utf-8')

def send_feishu_message(content: str, title: str = "", url: str = ""):
    """发送飞书卡片消息"""
    timestamp = int(datetime.now().timestamp())
    sign = gen_sign(WEBHOOK_SECRET, timestamp)
    
    card = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title or "告警通知"},
                "template": "red"
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": content}},
            ]
        }
    }
    
    resp = requests.post(WEBHOOK_URL, json=card)
    return resp.json()

# 使用示例
result = send_feishu_message(
    content="**AI分析结论：**服务器CPU异常，建议立即检查",
    title="🚨 HIGH 告警",
    url="https://你的系统/告警详情/123"
)
print(result)
```

## 环境变量配置

```bash
# .env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=***

DIFY_API_URL=https://api.dify.ai/v1
DIFY_API_KEY=app-xxx

SERVER_PUBLIC_IP=你的服务器公网IP
```

## 启动服务

```bash
# 安装依赖
pip install fastapi uvicorn httpx pydantic

# 启动
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 生产环境（使用 gunicorn）
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 飞书开发者后台配置

1. 打开 https://open.feishu.cn/app
2. 创建**企业自建应用** → 命名"告警助手"
3. 添加权限：
   - `im:message:readonly` - 接收消息
   - `im:message.send_as_bot` - 发送消息
4. 配置**事件订阅**：
   - 请求 URL: `http://你的服务器IP:8000/api/webhook/feishu`
   - 添加事件: `im.message.receive_v1`
5. 添加**自定义机器人**到目标群 → 获取 Webhook URL