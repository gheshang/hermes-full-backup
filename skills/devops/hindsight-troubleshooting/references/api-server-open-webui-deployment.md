# Hermes API Server + Open WebUI 部署指南

## 架构

```
┌─────────────┐     SSH隧道      ┌──────────────────────────┐
│ 本地浏览器   │◄────────────────►│  VPS (HKTJser0417215710)  │
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

## 前置条件

1. Hermes Gateway 运行中：`hermes gateway status`
2. 磁盘空间充足：`df -h /` 剩余 ≥ 10GB（Open WebUI 镜像 ~2-3GB + 运行时数据）
3. Docker 可用：`docker ps`

## 步骤 1：启用 API Server

```bash
# 生成强密码
PASS=$(openssl rand -base64 32 | tr -d '\n')

# 追加到 .env（用 >> 追加，不要用 > 覆盖！）
echo "" >> ~/.hermes/.env
echo "# API Server (for Open WebUI)" >> ~/.hermes/.env
echo "API_SERVER_ENABLED=true" >> ~/.hermes/.env
echo "API_SERVER_PORT=8642" >> ~/.hermes/.env
echo "API_SERVER_HOST=127.0.0.1" >> ~/.hermes/.env
echo "API_SERVER_KEY=$PASS" >> ~/.hermes/.env

# 验证
grep "API_SERVER" ~/.hermes/.env
```

**⚠️ 关键陷阱：用 `cat >` 覆盖 `.env` 会清空所有已有配置！** 必须用 `cat >>` 追加。

## 步骤 2：重启 Gateway

```bash
systemctl --user restart hermes-gateway.service
sleep 3

# 验证 Gateway 运行
hermes gateway status

# 验证 API Server 健康
curl -s http://127.0.0.1:8642/health
# 应返回: {"status": "ok", "platform": "hermes-agent"}

# 验证模型列表
curl -s http://127.0.0.1:8642/v1/models -H "Authorization: Bearer $PASS"
# 应返回: {"object": "list", "data": [{"id": "hermes-agent", ...}]}
```

## 步骤 3：部署 Open WebUI

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_BASE_URL=http://127.0.0.1:8642/v1 \
  -e OPENAI_API_KEY="$PASS" \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**首次启动注意事项：**
- Open WebUI 会从 HuggingFace 下载 embedding 和 reranker 模型（约 2-3GB）
- VPS 到 HuggingFace 网络可能很慢，首次启动可能需要 10-30 分钟
- 查看进度：`docker logs open-webui 2>&1 | tail -5`
- 容器健康状态：`docker ps | grep open-webui`（显示 "healthy" 即完成）

## 步骤 4：SSH 隧道（本地电脑）

```bash
ssh -N -L 3000:127.0.0.1:3000 hangskf@<服务器IP>
```

浏览器打开 `http://localhost:3000`，第一个注册用户自动成为管理员。

## 步骤 5：移动端访问（可选）

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

设置 Cloudflare Zero Trust Access Policy，用邮箱验证才能访问。

### 方案 B：frp/ngrok

需要公网服务器作为中转，配置较复杂，不推荐。

## 验证清单

| 检查项 | 命令 | 预期结果 |
|---|---|---|
| Gateway 运行 | `hermes gateway status` | `active (running)` |
| API Server 健康 | `curl http://127.0.0.1:8642/health` | `{"status": "ok"}` |
| 模型列表 | `curl http://127.0.0.1:8642/v1/models -H "Authorization: Bearer $PASS"` | 返回 `hermes-agent` |
| Open WebUI 容器 | `docker ps | grep open-webui` | `Up (healthy)` |
| Open WebUI API | `curl http://127.0.0.1:3000/api/config` | 返回配置 JSON |
| 磁盘空间 | `df -h /` | 剩余 ≥ 5GB |

## 卸载/清理

```bash
# 停止并删除容器
docker stop open-webui && docker rm open-webui

# 删除镜像
docker rmi ghcr.io/open-webui/open-webui:main

# 清理 Docker 残留
docker system prune -f

# 移除 API Server 配置
sed -i '/^API_SERVER_/d' ~/.hermes/.env

# 重启 Gateway 释放端口
systemctl --user restart hermes-gateway.service
```

## 常见问题

### Q: Open WebUI 容器启动后一直 "health: starting"

A: 首次启动需要从 HuggingFace 下载模型文件，VPS 网络慢时可能耗时 10-30 分钟。查看日志确认进度：
```bash
docker logs open-webui 2>&1 | grep -i "fetching\|downloading\|warning\|error"
```

### Q: API Server 返回 401 Unauthorized

A: API_SERVER_KEY 不匹配。检查 `.env` 中的值和 Open WebUI 的 `OPENAI_API_KEY` 环境变量是否一致。

### Q: 磁盘空间不足

A: 部署前必须检查 `df -h /`。如果剩余 < 5GB，先清理：
```bash
# Docker 清理
docker system prune -af --volumes

# uv 缓存清理
rm -rf ~/.local/share/uv/builds ~/.local/share/uv/index

# 查看大目录
du -sh /* 2>/dev/null | sort -hr | head -10
```

### Q: 无法从外网访问 Open WebUI

A: Open WebUI 默认绑定 `0.0.0.0:3000`，但 VPS 防火墙可能阻止。检查：
```bash
# 检查端口监听
ss -tlnp | grep 3000

# 检查防火墙
sudo ufw status  # 或 sudo firewall-cmd --list-all
```

如需外网访问，建议用 Cloudflare Tunnel 而不是直接暴露端口。
