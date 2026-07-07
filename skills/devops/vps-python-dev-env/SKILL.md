---
name: vps-python-dev-env
description: >-
  Set up a Python practice/learning environment on a headless VPS, including
  Jupyter Notebook with remote access via SSH tunnel, ngrok, Cloudflare Tunnel,
  or nginx reverse proxy (自有域名场景). Also covers building a MkDocs practice
  site from GitHub repos like Python-100-Days.
version: 1.4.0
author: 上河一号
metadata:
  hermes:
    tags: [vps, python, jupyter, ngrok, remote-access, dev-environment]
    category: devops
---

# VPS Python 开发环境搭建指南

用于在无公网端口开放的 VPS 上搭建可远程访问的 Python 练习环境 + Jupyter Notebook，支持从手机/平板等设备访问。

---

## 快速搭建流程

### 1. 创建工作目录 + 虚拟环境

```bash
mkdir -p ~/python-practice
python3 -m venv ~/python-practice/.venv
```

### 2. 安装常用包

```bash
~/python-practice/.venv/bin/pip install requests beautifulsoup4 pandas pytest jupyter
```

### 3. 启动 Jupyter

```bash
cd ~/python-practice && ~/python-practice/.venv/bin/jupyter notebook \
  --no-browser --ip=0.0.0.0 --port=8888
```

启动后在终端中找到 token URL：

```
http://127.0.0.1:8888/tree?token=<一串hash>
```

### 4. 后台运行（daemon 模式）

```bash
cd ~/python-practice
nohup ~/python-practice/.venv/bin/jupyter notebook \
  --no-browser --ip=0.0.0.0 --port=8888 > /dev/null 2>&1 &
```

## 远程访问方法

### 方法 A：SSH 隧道（推荐，含 autossh）

**适合有终端的环境（电脑、Termux）。** 不需要暴露端口到公网。

```bash
# 基础版
ssh -f -N -L 8888:localhost:8888 user@server-ip

# autossh（自动重连）
autossh -M 0 -f -N -L 8888:localhost:8888 user@server-ip
```

参数说明：
- `-f` → fork 到后台，关终端不中断
- `-N` → 只转发不执行命令（隧道专用）
- `-L a:b:c:d` → 本机 a 端口 → 远程 c 端口
- `-M 0` → autossh 用自己的心跳（不占端口）

**SSH config 快捷方式（~/.ssh/config）：**

```
Host pydev
    HostName server-ip
    User username
    LocalForward 8888 localhost:8888
```

之后只需 `ssh pydev`（加 `-f -N` 就是后台）。

**管理 SSH 隧道：**

```bash
# 看是否活着
ps aux | grep 'ssh.*8888'

# 关掉
ssh -O exit user@server-ip
# 或
pkill -f 'ssh.*8888.*localhost'
```

### 方法 B：ngrok（适合安卓平板 / iPad / 无终端的设备）

ngrok 把 VPS 的 Jupyter 端口暴露成一个公网 HTTPS URL，浏览器直接打开。

**在 VPS 上安装 ngrok：**

```bash
# 下载安装
cd /tmp
curl -sLO https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xzf ngrok-v3-stable-linux-amd64.tgz
mkdir -p ~/.local/bin && cp ngrok ~/.local/bin/

# 配置 authtoken（需要注册 https://dashboard.ngrok.com/signup）
# 登录后进 https://dashboard.ngrok.com/get-started/your-authtoken 复制 token
~/.local/bin/ngrok config add-authtoken <你的token>

# 启动隧道（把 VPS 8888 端口映射出去）
~/.local/bin/ngrok http 8888
```

启动后 ngrok 终端会打印 public URL：

```
Forwarding  https://xxxx.ngrok-free.app -> http://localhost:8888
```

用这个 HTTPS URL 打开即是 Jupyter。

**后台运行 ngrok：**

```bash
nohup ~/.local/bin/ngrok http 8888 --log=stdout > ~/ngrok.log 2>&1 &
```

查看 URL（不需要再看终端）：

```bash
curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
```

**停止 ngrok：**

```bash
pkill ngrok
```

### 方法 C：云平台安全组开放端口 + nginx 反向代理（推荐，同域名部署）

适合想要**一个域名下同时跑多个服务**（比如 MkDocs 文档站 + Jupyter Notebook）的场景。

**原理：** 服务器只开 80 端口（nginx 监听），nginx 根据路径转发：
- `/` → MkDocs/Material 静态文档站
- `/lab` → Jupyter Notebook（反向代理到 18080）

**要求：** 云平台安全组放行 80 端口（http），nginx 做反向代理。

**前置条件：安装 nginx**
```bash
sudo apt-get update && sudo apt-get install -y nginx
```

**1. 启动 Jupyter（带 base_url，让 nginx 能按路径转发）**
```bash
# 如果之前已经在运行，先停掉
pkill -f jupyter-notebook

# 用 base_url=/lab/ 重新启动
cd ~/python-practice && nohup ~/python-practice/.venv/bin/jupyter notebook \
  --no-browser --ip=0.0.0.0 --port=18080 \
  --NotebookApp.base_url=/lab/ > /dev/null 2>&1 &

# 确认启动
sleep 2 && ss -tlnp | grep jupyter
```

**2. 搭建 MkDocs 文档站**
```bash
cd ~/python-practice
git clone --depth 1 <你的文档仓库>  # 或准备现成 markdown
pip install mkdocs mkdocs-material
mkdir -p site
# 创建 mkdocs.yml，设置 docs_dir 指向文档目录
# cd site && mkdocs build
```

**3. 配置 nginx 反向代理**
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    # MkDocs 静态站点
    root /home/xxx/python-practice/site/site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # Jupyter Notebook 反向代理
    location /lab/ {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
        proxy_buffering off;
    }
}
```

**4. 生效**
```bash
sudo cp ~/python-practice/nginx-python-site.conf /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

**5. 在域名 DNS 控制台加 A 记录**
| 记录类型 | 主机记录 | 记录值 |
|---------|---------|-------|
| A | @ | 你的服务器公网 IP |

**6. 访问**
```
http://你的域名.com       → MkDocs 文档站
http://你的域名.com/lab   → Jupyter Notebook（用 token 登录）
```

**⚠️ Jupyter 权限问题：** nginx 以 www-data 用户运行，如果家目录权限是 750，nginx 进不去。修复：
```bash
chmod o+x /home/你的用户名
```

**⚠️ Jupyter token 获取：** 每次重启都会变，用以下命令查看：
```bash
ls -t ~/.local/share/jupyter/runtime/jpserver-*.json | head -1 | xargs cat | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])"
```

**方法 D：云平台安全组开放端口（不推荐，无反向代理）**

大多数云 VPS 的防火墙在平台层（安全组），不光在服务器内。如果非要直接暴露 8888 端口，需要去云控制台放行该端口的入站规则。

**不推荐的原因：** 直接暴露会增加安全风险，token 泄露则任何人可访问 Jupyter。

### 方法 D：Cloudflare Tunnel（推荐，国内访问优先）

当用户在中国大陆、服务器在境外时，ngrok 绕美国延迟高（300~500ms），Cloudflare Tunnel 借助亚太边缘节点（香港/新加坡/东京），延迟 50~100ms。Cloudflare Tunnel

**原理：** 服务器主动连 Cloudflare 边缘节点，不暴露任何入站端口。用户通过域名经 Cloudflare 访问。

**前置条件：** 一个域名（.xyz/.top 首年 ¥6~¥20，国外 Namecheap/Cloudflare Registrar 买不需要实名）。

**安装 cloudflared（在 VPS 上）：**

```bash
cd /tmp
curl -sLO https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
mkdir -p ~/.local/bin && mv cloudflared-linux-amd64 ~/.local/bin/cloudflared
```

**配置 Tunnel（在 VPS 上一次性操作）：**

```bash
# 1. 登录（浏览器打开 URL 授权你的 Cloudflare 账号）
~/.local/bin/cloudflared tunnel login

# 2. 创建隧道
~/.local/bin/cloudflared tunnel create jupyter-tunnel

# 3. 配置 DNS（隧道 ID 会在上一步打印，形如 <uuid>）
~/.local/bin/cloudflared tunnel route dns <tunnel-id> jupyter.你的域名.com

# 4. 启动隧道连接 Jupyter
~/.local/bin/cloudflared tunnel run --url http://127.0.0.1:8888 <tunnel-id>
```

之后访问 `https://jupyter.你的域名.com` 即可直达 Jupyter。

**后台运行：**

```bash
~/.local/bin/cloudflared tunnel run --url http://127.0.0.1:8888 <tunnel-id> > ~/cloudflared.log 2>&1 &
```

**停止：**

```bash
pkill cloudflared
```

### 方法 E：Nginx 反向代理（自有域名场景）

**适合有域名、服务器有公网 IP 的场景。** 同一个域名下可以同时跑：练习题库站（MkDocs/静态页面）+ Jupyter Notebook。

原理：`你的域名.com/` → 题库站（静态 HTML），`你的域名.com/lab/` → Jupyter。

**前置条件：**
- nginx 已安装、端口 80 可达
- 已买域名，DNS A 记录已指向服务器 IP（可访问）
- 服务器 80 端口已在云安全组放行

#### 1. 搭建题库站（可选，纯 Jupyter 可跳过）

```bash
# 克隆 Python-100-Days 或任何 Markdown 文档仓库
git clone --depth 1 https://github.com/jackfrued/Python-100-Days.git ~/python-practice/python-100-days

# 安装 MkDocs + Material 主题
~/python-practice/.venv/bin/pip install mkdocs mkdocs-material

# 在站点目录创建 mkdocs.yml，docs_dir 指向克隆目录
# 参考模板：~/.hermes/skills/devops/vps-python-dev-env/templates/mkdocs-practice-site.yml
```

MkDocs 会自动从目录结构生成导航。构建：

```bash
cd ~/python-practice/site && ~/python-practice/.venv/bin/mkdocs build
# 生成的静态文件在 ~/python-practice/site/site/
```

#### 2. Markdown → Notebook 转换（可选，让学员在 Jupyter 里直接运行例题）

把 Python-100-Days 中的 .md 文件批量转为 .ipynb，学员在 Jupyter 里打开即可逐段运行代码。

```bash
# 详细说明：~/.hermes/skills/devops/vps-python-dev-env/references/md-to-ipynb-conversion.md
# 转换脚本：~/.hermes/skills/devops/vps-python-dev-env/scripts/md-to-ipynb.py

python3 ~/.hermes/skills/devops/vps-python-dev-env/scripts/md-to-ipynb.py \
  ~/python-practice/python-100-days \
  ~/python-practice/nb/

# 输出在 ~/python-practice/nb/ 下，跟原目录结构一致
# 打开 /lab/ 后点进 nb/ 目录即可看到所有 .ipynb 文件
```

注意事项：
- ` ```python ` fenced code blocks → notebook code cell，其余文本 → markdown cell
- 纯概念文件（无代码块）→ 1 个 markdown cell，不影响浏览
- 4空格缩进的代码块保留在 markdown cell 中不做拆分
- 输出目录需要放在 Jupyter root_dir 下（默认 `~/python-practice/`）才可见

#### 3. 启动 Jupyter（带 base_url）

**关键：** 反向代理下 Jupyter 必须设置 `base_url`，否则页面内的资源链接会断。

```bash
pkill -f jupyter-notebook  # 先停掉旧的
cd ~/python-practice && exec ~/python-practice/.venv/bin/jupyter lab \
  --no-browser --ip=127.0.0.1 --port=18080 \
  --ServerApp.base_url=/lab/ \
  --ServerApp.allow_remote_access=True
```

💡 `ip=127.0.0.1`（不是 `0.0.0.0`）→ 只允许本机 nginx 访问，公网不能直连 Jupyter 端口，更安全。

获取 token：

```bash
cat ~/.local/share/jupyter/runtime/jpserver-*.json | grep token
```

#### 4. nginx 配置

```bash
# 配置模板在 ~/.hermes/skills/devops/vps-python-dev-env/scripts/nginx-mkdocs-jupyter.conf
# ⚠️ 复制前把模板中的 USERNAME 替换成你的服务器用户名，例如 hangskf
cp ~/.hermes/skills/devops/vps-python-dev-env/scripts/nginx-mkdocs-jupyter.conf /tmp/nginx.conf
sed 's/USERNAME/你的用户名/g' /tmp/nginx.conf | sudo tee /etc/nginx/sites-enabled/default > /dev/null
sudo nginx -t && sudo systemctl reload nginx
```

**⚠️ WebSocket：** Jupyter 需要 nginx 转发 WebSocket，否则页面加载后无法连接内核。模板中已包含 `Upgrade` 和 `Connection` 头。

**⚠️ 大文件/长运行：** Jupyter 运行长时间代码时需要 `proxy_read_timeout` 足够大（模板中设为 86400 秒=24 小时）且 `proxy_buffering off`。

#### 日常操作

| 操作 | 命令 |
|------|------|
| 构建题库站（Markdown 更新后） | `cd ~/python-practice/site && ~/python-practice/.venv/bin/mkdocs build` |
| 启动 Jupyter（反代模式） | `exec ~/python-practice/.venv/bin/jupyter notebook --no-browser --ip=127.0.0.1 --port=18080 --NotebookApp.base_url=/lab/` |
| 重启 nginx | `sudo nginx -t && sudo systemctl reload nginx` |
| 合并访问 | `http://你的域名.com/` → 题库站，`http://你的域名.com/lab/` → Jupyter |

#### 常见问题

- **Jupyter 页面空白/加载失败：** 大概率是 base_url 没设对。确认 `jpserver-*.json` 里 `base_url` 是 `/lab/`（尾部斜杠不可省）
- **内核连不上：** WebSocket 转发没配置好。检查 nginx 是否包含 `proxy_set_header Upgrade` 和 `Connection "upgrade"`
- **题库站图片不显示：** MkDocs 构建时会自动复制资源到 site/ 目录。确认 `mkdocs.yml` 的 `docs_dir` 指向包含 `res/` 目录的路径
- **nginx 返回 404 但文件确实存在：** 如果站点文件放在 `/home/用户名/` 下，检查 `/home/用户名` 权限是否为 `drwxr-x---`（750）——nginx 以 www-data 用户运行，无法 traverse 家目录。修复：`chmod o+x /home/用户名`（给 others 加执行权限，只允许进入，不开放 list，安全风险低）

---

## 第一件事：诊断端口是否可公网访问

部署完 Jupyter 后不要假设端口通了。先做诊断：

```bash
# 1. OS 防火墙检查
sudo ufw status 2>/dev/null || echo "ufw not active"
sudo iptables -L INPUT -n 2>/dev/null | grep ACCEPT | head -5

# 2. 监听确认
ss -tlnp | grep jupyter || echo "jupyter not listening"

# 3. 公网可达测试（在服务器上测公网 IP 是否通）
PUBLIC_IP=$(curl -s ifconfig.me)
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$PUBLIC_IP:8888/" 2>&1
# 返回 0xx / 空 → hypervisor 防火墙拦截了端口
# 返回 302 → 端口的通，Jupyter 正常响应

# 4. 端口试探：换一个非标准高端口试试
pkill -f jupyter-notebook
cd ~/python-practice && ~/python-practice/.venv/bin/jupyter notebook --no-browser --ip=0.0.0.0 --port=18080
# 还不行？测一下 80/443 是否也被拦
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$PUBLIC_IP:80/" 2>&1
```

```text
诊断结论对照表：
┌────────────────────┬──────────────────────────┐
│ OS端口OK + 公网不通 │ 云厂商 hypervisor 防火墙  │
├────────────────────┼──────────────────────────┤
│ 公网不通（含80/443）│ 安全组挡了所有入站流量     │
├────────────────────┼──────────────────────────┤
│ 公网80/443通，其    │ 安全组只开放了基本端口     │
│ 他不通              │                          │
└────────────────────┴──────────────────────────┘
```

如果诊断结果是"hypervisor 防火墙拦截且没有安全组控制台"，直接走 **方法 D（Cloudflare Tunnel）**。

## 日常操作

| 操作 | 命令 |
|------|------|
| 启动 Jupyter | `nohup ~/python-practice/.venv/bin/jupyter-notebook --no-browser --ip=0.0.0.0 --port=8888 > /dev/null 2>&1 &` |
| 查看是否在运行 | `ss -tlnp \| grep jupyter` |
#### vps-python-dev-env/SKILL.md

---

#### 踩坑记录

| 坑 | 解决 |
|----|------|
| Jupyter 启动后没输出/退出了 | 不要用 `source .venv/bin/activate` 来启动后台进程，直接用 `.venv/bin/jupyter-notebook` 全路径 |
| 端口被占用 | 自动换端口或先 `pkill -f jupyter-notebook` |
| ngrok 提示需要 authtoken | 必须去 ngrok dashboard 注册拿 token，免费版够用 |
| 安卓平板没终端 | 装 Termux（F-Droid 版），跑 SSH 隧道；或用 ngrok 方案 |
| SSH 隧道一关终端就断 | 加 `-f` 参数：`ssh -f -N -L ...` |
| Jupyter token 每次重启都变 | 无法在无交互环境设固定密码；推荐用 SSH 隧道方式（不暴露端口，不需要 token 重复输入） |
| **nginx 反向代理 Jupyter 时 403 Forbidden** | Jupyter 默认拒绝非本地 Host 头的请求（`ServerApp.allow_remote_access` 默认 False）。nginx 反代时 `Host` 头是域名，Jupyter 视为远程访问返回 403。启动命令加 `--ServerApp.allow_remote_access=True` |
| **nginx 报 403/404 无权访问家目录** | `/home/xxx` 权限默认 750（others 无权限），nginx 以 www-data 运行进不去。执行 `chmod o+x /home/xxx` |
| **nginx 配置端口冲突** | 确保 80 端口未被其他服务占用：`ss -tlnp \| grep ':80 '` |

---

## 扩展：把教程/文档仓库变成浏览式学习站

当你在学 Python 教程（如 Python-100-Days）时，可以把它转成一个 Material 主题的文档站 + Jupyter Notebook 放在同一个域名下。

### 流程

```bash
# 1. 克隆仓库
git clone --depth 1 https://github.com/jackfrued/Python-100-Days.git ~/python-practice/python-100-days

# 2. 安装 MkDocs + Material
~/python-practice/.venv/bin/pip install mkdocs mkdocs-material

# 3. 创建 mkdocs.yml 站点配置
mkdir ~/python-practice/site
cat > ~/python-practice/site/mkdocs.yml << 'YAML'
site_name: Python 100 天练习
theme:
  name: material
  features:
    - navigation.instant
    - content.code.copy
docs_dir: ../python-100-days
strict: false
YAML

# 4. 构建站点
cd ~/python-practice/site && ~/python-practice/.venv/bin/mkdocs build

# 5. nginx 配置：/ → 文档站，/lab/ → Jupyter
```

详细步骤见技能 `jupyter-server-headless` 中的「Serving Jupyter Behind nginx Reverse Proxy」章节。

### 批量将 Markdown 转为 Jupyter Notebook（.ipynb）

参考脚本 `~/python-practice/convert_md_to_nb.py`，原理：

```python
import nbformat as nbf
import re

def split_markdown(md_text):
    """将 markdown 按代码块分段，返回 [(type, content), ...]"""
    pattern = re.compile(r'(?s)```(\w*)\n(.*?)```')
    segments, last_end = [], 0
    for match in pattern.finditer(md_text):
        lang, code = match.groups()
        if match.start() > last_end:
            text = md_text[last_end:match.start()].strip()
            if text:
                segments.append(('markdown', text))
        if lang in ('', 'python', 'py', 'Python'):
            segments.append(('code', code.strip()))
        else:
            segments.append(('markdown', f"```{lang}\n{code}```"))
        last_end = match.end()
    remaining = md_text[last_end:].strip()
    if remaining:
        segments.append(('markdown', remaining))
    return segments

def convert_md_to_ipynb(md_path, nb_path):
    segments = split_markdown(open(md_path).read())
    if not segments:
        return False
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_code_cell(c) if t == 'code'
                else nbf.v4.new_markdown_cell(c)
                for t, c in segments]
    os.makedirs(os.path.dirname(nb_path), exist_ok=True)
    nbf.write(nb, nb_path)
    return True
```

## 安全提醒

- **不要**把 Jupyter 的 token 发给不信任的人
- **不要**在 ngrok URL 上输敏感密码（ngrok 免费版是公网可扫的）
- SSH 隧道最安全：不暴露任何端口到公网
- ngrok 次之：HTTPS 加密但 URL 随机，有一定隐蔽性
- 直接开端口最不安全，除非配合 IP 白名单
