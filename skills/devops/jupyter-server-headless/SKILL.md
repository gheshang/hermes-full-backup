---
name: jupyter-server-headless
description: >
  Set up and run Jupyter Notebook as a user-facing service on a headless Linux
  VPS. Covers virtual environment creation, package installation, background
  server start, token discovery, port conflict resolution, and firewall check.
  Use when the user wants to access Jupyter from their browser on a remote server
  (no GUI, no X forwarding).
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jupyter, notebook, headless, vps, python, environment]
    category: devops
---

# Jupyter Server on Headless VPS

Set up Jupyter so the user can open it in their browser from any machine.

## Three Key Variants

| Scenario | Command |
|----------|---------|
| **Jupyter Notebook** (classic) | `.venv/bin/jupyter notebook --no-browser --ip=0.0.0.0 --port=8888` |
| **JupyterLab** (modern, this user) | `.venv/bin/jupyter lab --no-browser --ip=127.0.0.1 --port=18080 --ServerApp.base_url=/lab/` |
| Behind nginx (same domain) | `.venv/bin/jupyter lab --no-browser --ip=127.0.0.1 --port=18080 --ServerApp.base_url=/lab/ --ServerApp.allow_remote_access=True` |

Key config difference: JupyterLab uses `--ServerApp.base_url=/lab/`, classic Notebook uses `--NotebookApp.base_url=/notebook/`. Both still work in recent versions, but `ServerApp` is the canonical config path for JupyterLab.

## Quick Start (Summary)

```bash
# 1. Create dir + venv
mkdir -p ~/python-practice
python3 -m venv ~/python-practice/.venv

# 2. Install Jupyter + common packages
~/python-practice/.venv/bin/pip install notebook pandas requests beautifulsoup4

# 3. Start (use full binary path, not source activate)
#    - 无反代: ip=0.0.0.0 监听所有网卡
#    - 后端有 nginx 反代: ip=127.0.0.1 + base_url 设置
cd ~/python-practice && exec ~/python-practice/.venv/bin/jupyter notebook \
  --no-browser --ip=0.0.0.0 --port=8888 2>&1

# 4. Get token
cat ~/.local/share/jupyter/runtime/jpserver-*.html

# 5. Check firewall
sudo ufw status 2>/dev/null || echo "ufw not active"
```

## Detailed Workflow

### 1. Create Environment

```bash
mkdir -p ~/python-practice
python3 -m venv ~/python-practice/.venv
```

### 2. Install Packages

Always use the venv's pip directly (not `source activate`):

```bash
~/python-practice/.venv/bin/pip install notebook pandas requests beautifulsoup4 pytest jupyter
```

### 3. Start Jupyter Server

Start as a **background process** (the server never exits on its own):

```bash
cd ~/python-practice && exec ~/python-practice/.venv/bin/jupyter notebook \
  --no-browser --ip=0.0.0.0 --port=8888 2>&1
```

Key points:
- `exec` replaces the shell, giving Jupyter PID 1 in the bg process
- Use the **full path** to the venv binary — `source .venv/bin/activate` does NOT work in background processes (non-interactive shell)
- `--no-browser` — no GUI to open
- `--ip=0.0.0.0` — listen on all interfaces so external access works
- `--port=8888` — can change to an available port

### 4. Discover Access Token

Jupyter generates a random token on startup. You cannot see it from the
background process output. Retrieve it from the runtime directory:

```bash
cat ~/.local/share/jupyter/runtime/jpserver-*.html
```

This file contains a redirect page with the full URL including token.

Alternatively, parse it from the HTML:

```bash
grep -oP 'token=\K[a-f0-9]+' ~/.local/share/jupyter/runtime/jpserver-*.html | head -1
```

### 5. Construct Access URL

Replace `0.0.0.0` with the server's public IP:

```bash
PUBLIC_IP=$(curl -s ifconfig.me)
TOKEN=$(grep -oP 'token=\K[a-f0-9]+' ~/.local/share/jupyter/runtime/jpserver-*.html | head -1)
echo "http://$PUBLIC_IP:8888/tree?token=$TOKEN"
```

### 6. Firewall Check

```bash
sudo ufw status 2>/dev/null || echo "ufw not active"
iptables -L INPUT -n --line-numbers 2>/dev/null | grep ACCEPT | head -10
```

### 7. Stop Jupyter

```bash
pkill -f jupyter-notebook
```

## Pitfalls

### ❌ Jupyter token changes on every restart

Each restart generates a new random token. Always re-read the runtime directory after start.

### ❌ `jupyter-notebook` not on PATH

When starting via venv, don't rely on PATH. Use the exact path:
`~/python-practice/.venv/bin/jupyter notebook`

### ❌ `/home/` permission blocking nginx access

When nginx runs as www-data and serves files from `/home/user/`, the home directory must be traversable:
```bash
chmod o+x /home/hangskf
```
Without this, nginx returns 404 even though the files exist and are readable.

### ❌ Cloud provider firewall（最常见）

OS 防火墙（ufw/iptables）没有阻挡，但公网仍然打不开 → 云厂商 hypervisor 层的防火墙/安全组拦了。

诊断：
```bash
PUBLIC_IP=$(curl -s ifconfig.me)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$PUBLIC_IP:8888/"
```
- 0xx / 空 → hypervisor 防火墙拦截
- 302 → 端口通的，Jupyter 正常响应

推荐走 **SSH 隧道** 或 **Cloudflare Tunnel**（中国访问境外 VPS 的场景）。

### ❌ `source .venv/bin/activate` in background processes

Does not work in background processes. Always use full venv binary path:
```bash
# WRONG
source .venv/bin/activate && jupyter notebook ...

# RIGHT
~/python-practice/.venv/bin/jupyter notebook ...
```

### ❌ Port already in use

```bash
pkill -f jupyter-notebook
sleep 1
ss -tlnp | grep -E '888[0-9]' || echo "ports clear"
```

### ❌ Can't set password non-interactively

`jupyter notebook password` calls `getpass.getpass()` which fails in
non-interactive terminals. Use token-based auth.

## Serving Jupyter Behind nginx Reverse Proxy (Same Domain)

When Jupyter and a static site share one domain, use nginx to route `/` → static site, `/lab/` → Jupyter.

### 1. Restart Jupyter with base_url + allow_remote_access

Jupyter defaults to blocking non-local `Host` headers (returns 403). When proxied through nginx, the original `Host` (e.g. `hangskf.xyz`) passes through — Jupyter treats it as remote access. Fix: add `--ServerApp.allow_remote_access=True`.

```bash
pkill -f jupyter
cd ~/python-practice && exec ~/python-practice/.venv/bin/jupyter lab \
  --no-browser --ip=127.0.0.1 --port=18080 \
  --ServerApp.base_url=/lab/ \
  --ServerApp.allow_remote_access=True
```

### 2. nginx Config

```nginx
server {
    listen 80 default_server;
    server_name _;

    # Static site at /
    root /home/user/python-practice/site/site;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }

    # Jupyter at /lab/
    location /lab/ {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket (Jupyter needs this)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
        proxy_buffering off;
    }

    # Jupyter static assets (cache)
    location ~* /lab/static/ {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Save as `~/python-practice/nginx-jupyter.conf`, then:
```bash
sudo cp ~/python-practice/nginx-jupyter.conf /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

### 3. Token Retrieval (After Restart)

```bash
ls -t ~/.local/share/jupyter/runtime/jpserver-*.json | head -1 | xargs cat
# Look for "token" field
```

### ❌ Missing base_url behind reverse proxy — static assets 404

When nginx/Caddy proxies `/lab/` → Jupyter, Jupyter MUST know the path prefix.

```bash
# WRONG — pages load but images/links/kernel WebSocket all 404
exec .../jupyter notebook --no-browser --ip=127.0.0.1 --port=18080

# RIGHT
exec .../jupyter lab --no-browser --ip=127.0.0.1 --port=18080 \
  --ServerApp.base_url=/lab/
```

Verify: `cat ~/.local/share/jupyter/runtime/jpserver-*.json` → `base_url` field must match the nginx location prefix (include trailing slash).

Also: when behind nginx, bind to `127.0.0.1` not `0.0.0.0` — nginx is the only thing that should hit Jupyter directly, and it runs on the same host.

### ❌ 403 Forbidden through nginx reverse proxy — Host header blocked

**Symptom**: nginx returns `502 Bad Gateway` check passes (backend is running), but browser shows **403 Forbidden**. Jupyter access log shows:
```
Blocking request with non-local 'Host' hangskf.xyz
403 GET /lab/static/favicon.ico
```

**Cause**: Jupyter's default security policy rejects non-local `Host` headers. When nginx proxies requests, it passes the original `Host` header (e.g. `hangskf.xyz`) — Jupyter treats this as a remote access attempt.

**Fix**: Start Jupyter with `--ServerApp.allow_remote_access=True`:
```bash
exec .../jupyter lab --no-browser --ip=127.0.0.1 --port=18080 \
  --ServerApp.base_url=/lab/ \
  --ServerApp.allow_remote_access=True
```

**Diagnosis**: Check Jupyter's own log output (not nginx error log) for "Blocking request with non-local 'Host'" warnings. The 403 response body may not show the cause — the Jupyter process stdout/stderr has the real message.

## Verification

```bash
ss -tlnp | grep jupyter        # listening?
ls ~/.local/share/jupyter/runtime/jpserver-*.html  # token file exists?
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8888/api  # 403 = alive
```

## Operational Monitoring: Jupyter Crashed / Won't Start

### Symptoms

| Symptom | Cause |
|---------|-------|
| `502 Bad Gateway` from nginx at `/lab/` | Jupyter process died. nginx proxy returns 502 when backend is unreachable. |
| `curl: (7) Connection refused` on direct port | No process bound to the port. |
| `ss -tlnp` shows nothing on expected port | Process terminated. |

### Restart Procedure

```bash
# 1. Kill any existing jupyter processes
pkill -f "jupyter"

# 2. Verify port is free
ss -tlnp | grep 18080 || echo "port free"

# 3. Start again (full venv path, never source activate)
#    Add --ServerApp.allow_remote_access=True when behind nginx
cd ~/python-practice && exec ~/python-practice/.venv/bin/jupyter lab \
  --no-browser --ip=127.0.0.1 --port=18080 \
  --ServerApp.base_url=/lab/ \
  --ServerApp.allow_remote_access=True 2>&1

# 4. Wait 3s, then verify
sleep 3
ss -tlnp | grep 18080
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18080/lab/  # expect 302
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/lab/       # expect 302 via nginx
```

### Persistent Service (Prevents Future Crashes)

Make Jupyter survive reboots via systemd user service:

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/jupyter.service << 'SERVICEEOF'
[Unit]
Description=JupyterLab
After=network.target

[Service]
ExecStart=%h/python-practice/.venv/bin/jupyter lab --no-browser --ip=127.0.0.1 --port=18080 --ServerApp.base_url=/lab/
WorkingDirectory=%h/python-practice
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
SERVICEEOF

systemctl --user daemon-reload
systemctl --user enable --now jupyter.service
systemctl --user status jupyter.service
```

Note: `--ServerApp.base_url` for JupyterLab, `--NotebookApp.base_url` for classic Notebook.