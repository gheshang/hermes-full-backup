---
name: python-practice-environment
description: Set up a Python learning environment with Jupyter Notebook on a remote Ubuntu server, accessible from mobile devices (Android tablets, phones).
---

# Python Practice Environment Setup

Set up a Python learning environment on a remote Ubuntu server, with Jupyter Notebook accessible from any device (including Android tablets via browser).

## Trigger

User says: "want to practice Python", "set up Jupyter", "need a Python environment", "want to learn Python on the server".

## Steps

### 1. Create workspace and virtual environment

```bash
mkdir -p ~/python-practice
python3 -m venv ~/python-practice/.venv
```

### 2. Install common learning packages

```bash
~/python-practice/.venv/bin/pip install requests beautifulsoup4 pandas jupyter pytest matplotlib
```

⚠️ Packages install serially. On slow connections, install core packages first, then data-science packages in a second pass to avoid timeout.

### 3. Start Jupyter Notebook

```bash
cd ~/python-practice
~/python-practice/.venv/bin/jupyter notebook --no-browser --ip=0.0.0.0 --port=18080
```

- Use port 18080 (avoids common blocked ports like 8888)
- `--ip=0.0.0.0` binds to all interfaces
- Save the token from the output for user access

Background mode:

```bash
# Create startup script
cat > ~/python-practice/start_jupyter.sh << 'SCRIPT'
#!/bin/bash
cd /home/hangskf/python-practice
exec /home/hangskf/python-practice/.venv/bin/jupyter notebook --no-browser --ip=0.0.0.0 --port=18080
SCRIPT
chmod +x ~/python-practice/start_jupyter.sh

# Launch in background (via Hermes terminal with background=true)
bash ~/python-practice/start_jupyter.sh > /tmp/jupyter.log 2>&1
```

### 4. Handle external access

Four strategies, in order of preference:

#### A. Direct port access (if cloud firewall allows)

User opens inbound TCP rule in cloud provider's security group/ firewall:
- Protocol: TCP
- Port: 18080
- Source: 0.0.0.0/0
- Direction: Inbound

Test from inside server fails due to hairpin NAT. **Tell user to test from their own browser directly.**

#### B. SSH tunnel

For users with local terminal access (laptop):
```bash
ssh -f -N -L 18080:localhost:18080 user@server-ip
```
Then open `http://localhost:18080`.

Autossh for auto-reconnect:
```bash
autossh -M 0 -f -N -L 18080:localhost:18080 user@server-ip
```

#### C. Cloudflare Tunnel (best for mobile/China access)

Requires a domain. Server connects outbound to Cloudflare — no open ports needed.

```bash
# Install cloudflared
# Configure tunnel to forward localhost:18080
# User accesses via https://subdomain.domain.com
```

#### D. ngrok (quick but slow from China)

```bash
# Requires ngrok auth token from dashboard.ngrok.com
ngrok http 18080
```
Gives a public `https://xxx.ngrok-free.app` URL. US nodes only — **high latency from China (300-500ms)**.

## Port picking

Default cloud provider blocks: 8888 (Jupyter default), 8080, 80, 443 (varies).
Try: 18080, 23456, or other high ports >10000.

## Mobile (Android) access patterns

- **Android tablet without terminal**: Must use direct browser access (strategy A or C above). Cannot run SSH tunnel natively.
- **Android with Termux**: Can run SSH tunnel via `pkg install openssh && ssh -f -N -L ...`
- **Browser bookmark**: Save URL with token: `http://server-ip:18080/tree?token=xxx`

## Pitfalls

- **Hairpin NAT**: Curl from server to own public IP fails. Don't interpret as "port blocked". Have the user test from their actual device.
- **Jupyter token changes on restart**: Always extract and pass the new token. Have user bookmark the URL for convenience.
- **No auto-start on reboot**: Jupyter won't survive server reboot. For persistent setup, add a systemd service or cron @reboot.
- **HTTP, not HTTPS**: Token is transmitted in plaintext. Same-network sniffing risk. For production, front with nginx + Let's Encrypt.
- **Security group 方向**: Users often open outbound instead of inbound. Double-check direction and protocol (TCP).
- **云厂商后台生效延迟**: Security group changes may take 1-5 minutes to propagate.

## Verification

```bash
# Check Jupyter is listening
ss -tlnp | grep 18080

# Check token in log
grep -o 'token=[a-f0-9]*' /tmp/jupyter.log

# Verify locally (not via public IP)
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18080/
# Expected: 302
```

## Files created

| Path | Purpose |
|---|---|
| `~/python-practice/` | Workspace directory |
| `~/python-practice/.venv/` | Isolated Python virtual environment |
| `~/python-practice/start_jupyter.sh` | Reusable startup script |
| `/tmp/jupyter.log` | Runtime log (contains URL + token) |