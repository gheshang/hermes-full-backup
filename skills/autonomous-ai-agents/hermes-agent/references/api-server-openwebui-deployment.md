# Hermes API Server + Open WebUI 部署指南

**会话日期：** 2026-05-05  
**场景：** 通过 Web UI（Open WebUI）访问 Hermes Agent，而非终端 CLI

---

## 架构

```
┌─────────────┐     SSH隧道      ┌──────────────────────────┐
│ 本地浏览器   │◄────────────────►│  VPS                     │
│ localhost:3000│                │                          │
└─────────────┘                │  ┌────────────────────┐   │
                               │  │ Open WebUI :3000   │   │
                               │  │        ↓           │   │
                               │  │ Hermes API :8642   │   │
                               │  │        ↓           │   │
                               │  │ Hermes Gateway     │   │
                               │  │ (飞书/微信等)       │   │
                               │  └────────────────────┘   │
                               └──────────────────────────┘
```

Open WebUI 通过 OpenAI 兼容 API 协议连接 Hermes API Server，Hermes 处理请求并返回带工具调用进度的流式响应。

---

## 前置检查

**⚠️ 关键陷阱：不要假设 API Server 存在就直接配置**

部署前必须先验证 API Server 功能是否存在：

```bash
# 1. 检查官方文档
curl -s https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server | head -50

# 2. 检查源代码确认实现
grep -rn "API_SERVER" ~/.hermes/hermes-agent/gateway/platforms/api_server.py | head -5

# 3. 确认环境变量支持
grep -n "API_SERVER_ENABLED" ~/.hermes/hermes-agent/gateway/config.py
```

如果以上任一检查失败，说明当前版本的 Hermes Agent 可能不支持 API Server，需先升级或寻找替代方案。

---

## 部署步骤

### Step 1：启用 API Server

在 `~/.hermes/.env` 中添加（**用 `>>` 追加，不要覆盖**）：

```bash
PASS=$(openssl rand -base64 32 | tr -d '\n')
echo "API_SERVER_ENABLED=true" >> ~/.hermes/.env
echo "API_SERVER_PORT=8642" >> ~/.hermes/.env
echo "API_SERVER_HOST=0.0.0.0" >> ~/.hermes/.env
echo "API_SERVER_KEY=$PASS" >> ~/.hermes/.env
```

**注意：**
- `API_SERVER_HOST=0.0.0.0` 是必须的，因为 SSH 隧道需要绑定到非 localhost 地址
- 当绑定到非 localhost 时，`API_SERVER_KEY` 是强制要求的
- 记下 `$PASS` 的值，后面 Open WebUI 要用

### Step 2：重启 Gateway

```bash
systemctl --user restart hermes-gateway.service
sleep 3
hermes gateway status
```

**验证 API Server 启动：**

```bash
curl -s http://127.0.0.1:8642/health
# 预期: {"status": "ok"}

curl -s http://127.0.0.1:8642/v1/models \
  -H "Authorization: Bearer $PASS"
# 预期: {"object": "list", "data": [{"id": "hermes-agent", ...}]}
```

### Step 3：部署 Open WebUI

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_BASE_URL=http://127.0.0.1:8642/v1 \
  -e OPENAI_API_KEY="$PASS" \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**Docker 内网访问注意：** 如果 Open WebUI 容器需要访问宿主机的 API Server，使用 `host.docker.internal`：

```bash
-e OPENAI_API_BASE_URL=http://host.docker.internal:8642/v1
```

### Step 4：SSH 隧道（本地电脑执行）

```bash
ssh -N -L 8642:127.0.0.1:8642 -L 3000:127.0.0.1:3000 hangskf@<服务器IP>
```

浏览器打开 `http://localhost:3000`，第一个注册的用户自动成为管理员。

---

## API Server 端点参考

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | 标准 OpenAI Chat Completions 格式 |
| `/v1/responses` | POST | OpenAI Responses API 格式，支持 `previous_response_id` |
| `/v1/runs` | POST | 长会话流式进度订阅 |
| `/v1/models` | GET | 列出可用模型（默认 `hermes-agent`） |
| `/v1/capabilities` | GET | API 功能清单 |
| `/health` | GET | 健康检查 |
| `/health/detailed` | GET | 详细指标 |

---

## 移动端访问方案

### 方案 A：Cloudflare Tunnel（推荐）

```bash
# 安装 cloudflared
curl -L --fail https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared

# 登录并创建隧道
cloudflared tunnel login
cloudflared tunnel create hermes-webui
cloudflared tunnel route dns hermes-webui hermes.yourdomain.com

# 配置路由
cat > ~/.cloudflared/config.yml << EOF
tunnels:
  hermes-webui:
    credentials-file: /home/hangskf/.cloudflared/xxx.json
    ingress:
      - hostname: hermes.yourdomain.com
        service: http://127.0.0.1:3000
      - service: http_status:404
EOF

cloudflared tunnel run hermes-webui &
```

**安全：** 设置 Cloudflare Zero Trust Access Policy，用邮箱验证才能访问。

### 方案 B：Termux SSH 隧道（Android）

```bash
pkg install openssh
ssh -N -L 3000:127.0.0.1:3000 hangskf@<服务器IP>
```

浏览器打开 `http://localhost:3000`。

---

## 已知限制

| 限制 | 详情 |
|------|------|
| 文件上传 | `/v1/chat/completions` 不支持 `file`/`input_file`/`file_id`，返回 400 |
| `previous_response_id` | 仅在 `/v1/responses` 中支持，`/v1/chat/completions` 不支持 |
| CORS | 默认禁用，需显式设置 `API_SERVER_CORS_ORIGINS` |
| 模型名称 | 默认为 profile 名或 `hermes-agent` |

---

## 故障排查

### API Server 未启动

```bash
# 检查 Gateway 日志
journalctl --user -u hermes-gateway.service -n 50 --no-pager

# 检查端口监听
ss -tlnp | grep 8642

# 检查 .env 配置
grep "API_SERVER" ~/.hermes/.env
```

### Open WebUI 无法连接

```bash
# 从容器内测试
docker exec open-webui curl -s http://host.docker.internal:8642/health

# 从宿主机测试
curl -s http://127.0.0.1:8642/health
```

### API 认证失败

```bash
# 验证 API key
curl -s http://127.0.0.1:8642/v1/models \
  -H "Authorization: Bearer $PASS"

# 检查 key 是否匹配
grep "API_SERVER_KEY" ~/.hermes/.env
```

---

## 相关文档

- [Hermes API Server 官方文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server)
- [Open WebUI 连接 Hermes Agent 指南](https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/)
