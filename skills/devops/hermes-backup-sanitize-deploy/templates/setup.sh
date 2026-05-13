#!/usr/bin/env bash
# ============================================================================
# Hermes Agent + Hindsight + CC Switch + Claude Code — One-Click Setup
# ============================================================================
# 不用 set -e：安装步骤允许失败，靠后续检查 + 诊断信息引导用户
# 不吞 stderr：让用户看到失败原因，而不是静默失败
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC} $*"; }
ok() { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err() { echo -e "${RED}[ERR]${NC} $*" >&2; }

SKIP_HERMES=false; SKIP_HINDSIGHT=false; SKIP_CC_SWITCH=false
HERMES_REPO="${HERMES_REPO:-https://github.com/NousResearch/hermes-agent.git}"
HERMES_BRANCH="${HERMES_BRANCH:-main}"
HERMES_FAILED=false

for arg in "$@"; do
 case "$arg" in
 --skip-hermes) SKIP_HERMES=true ;;
 --skip-hindsight) SKIP_HINDSIGHT=true ;;
 --skip-cc-switch) SKIP_CC_SWITCH=true ;;
 --hermes-repo=*) HERMES_REPO="${arg#*=}" ;;
 --hermes-branch=*) HERMES_BRANCH="${arg#*=}" ;;
 esac
done

# ── Ensure ~/.local/bin in PATH ──────────────────────────────────────────────
LOCAL_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
 info "Adding $LOCAL_BIN to PATH..."
 export PATH="$LOCAL_BIN:$PATH"
 if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo "" >> "$HOME/.bashrc"
  echo "# Added by Hermes setup" >> "$HOME/.bashrc"
  echo "export PATH=\"$LOCAL_BIN:\$PATH\"" >> "$HOME/.bashrc"
  ok "Added to ~/.bashrc (permanent)"
 fi
 ok "PATH updated for this session"
fi

# ── Check prerequisites ──────────────────────────────────────────────────────
info "Checking prerequisites..."
MISSING_PREREQ=false

if ! command -v python3 &>/dev/null; then
 err "python3 not found!"
 err "Install: sudo apt install python3 python3-pip python3-venv"
 MISSING_PREREQ=true
else
 PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
 info "python3: $PY_VER ($(which python3))"
 if python3 -c "import venv" 2>/dev/null; then
  info "python3-venv: OK"
 else
  warn "python3-venv missing, trying to install..."
  sudo apt-get install -y python3-venv 2>/dev/null || sudo yum install -y python3-venv 2>/dev/null || {
   err "python3-venv install failed. Run manually: sudo apt install python3-venv"
   MISSING_PREREQ=true
  }
 fi
fi

if ! command -v git &>/dev/null; then
 err "git not found!"
 err "Install: sudo apt install git"
 MISSING_PREREQ=true
else
 info "git: $(git --version 2>/dev/null || echo 'unknown')"
fi

if [ "$MISSING_PREREQ" = true ]; then
 err "Missing prerequisites. Install them first, then re-run this script."
 exit 1
fi

# ── Hermes Agent ──────────────────────────────────────────────────────────────
HERMES_BIN_IN_VENV="$HERMES_HOME/hermes-agent/venv/bin/hermes"

if [ "$SKIP_HERMES" = false ]; then
 info "Installing Hermes Agent..."

 # 即使venv里已有hermes，也确保symlink存在（修复"已安装但命令找不到"的问题）
 if [ -f "$HERMES_BIN_IN_VENV" ]; then
  info "Hermes venv found at $HERMES_BIN_IN_VENV, ensuring symlink..."
  mkdir -p "$LOCAL_BIN"
  ln -sf "$HERMES_BIN_IN_VENV" "$LOCAL_BIN/hermes"
  ok "Symlink: $LOCAL_BIN/hermes -> $HERMES_BIN_IN_VENV"
 fi

 if command -v hermes &>/dev/null; then
  ok "Hermes installed: $(hermes --version 2>/dev/null || echo 'version unknown')"
 else
  # hermes-agent is NOT on PyPI — must install from GitHub source
  info "Cloning from $HERMES_REPO (branch: $HERMES_BRANCH)..."
  if [ -d "$HERMES_HOME/hermes-agent" ]; then
   info "Existing source found, pulling updates..."
   git -C "$HERMES_HOME/hermes-agent" pull || warn "git pull failed, using existing source"
  else
   if ! git clone -b "$HERMES_BRANCH" "$HERMES_REPO" "$HERMES_HOME/hermes-agent"; then
    err "git clone failed! Check network or repo URL."
    err "If behind GFW, try: HERMES_REPO=https://ghproxy.com/https://github.com/NousResearch/hermes-agent.git bash setup.sh"
    HERMES_FAILED=true
   fi
  fi

  if [ "$HERMES_FAILED" = false ]; then
   info "Creating venv..."
   if ! python3 -m venv "$HERMES_HOME/hermes-agent/venv"; then
    err "venv creation failed! Check python3-venv is installed."
    HERMES_FAILED=true
   fi
  fi

  if [ "$HERMES_FAILED" = false ]; then
   info "Installing hermes-agent into venv (1-2 min)..."
   "$HERMES_HOME/hermes-agent/venv/bin/pip" install --upgrade pip 2>&1 | tail -1
   if ! "$HERMES_HOME/hermes-agent/venv/bin/pip" install -e "$HERMES_HOME/hermes-agent"; then
    err "pip install failed! Check error output above."
    err "Common causes: network timeout, missing build deps (gcc/libffi-dev)"
    err "Try: sudo apt install gcc libffi-dev && re-run"
    HERMES_FAILED=true
   fi
  fi

  if [ "$HERMES_FAILED" = false ]; then
   if [ -f "$HERMES_BIN_IN_VENV" ]; then
    mkdir -p "$LOCAL_BIN"
    ln -sf "$HERMES_BIN_IN_VENV" "$LOCAL_BIN/hermes"
    ok "Symlink created: $LOCAL_BIN/hermes -> $HERMES_BIN_IN_VENV"
   else
    err "hermes executable not found in venv!"
    err "Check: ls -la $HERMES_HOME/hermes-agent/venv/bin/"
    HERMES_FAILED=true
   fi
  fi

  if [ "$HERMES_FAILED" = false ] && command -v hermes &>/dev/null; then
   ok "Hermes installed successfully: $(hermes --version 2>/dev/null)"
  else
   err "Hermes installation failed. Manual steps:"
   err "  git clone $HERMES_REPO $HERMES_HOME/hermes-agent"
   err "  cd $HERMES_HOME/hermes-agent"
   err "  python3 -m venv venv && ./venv/bin/pip install -e ."
   err "  ln -sf $HERMES_HOME/hermes-agent/venv/bin/hermes $LOCAL_BIN/hermes"
  fi
 fi
fi

# ── Restore config files ─────────────────────────────────────────────────────
info "Restoring config files to $HERMES_HOME..."
mkdir -p "$HERMES_HOME"
cp "$SCRIPT_DIR/config.yaml" "$HERMES_HOME/config.yaml" 2>/dev/null || warn "config.yaml not found in backup"
cp "$SCRIPT_DIR/SOUL.md" "$HERMES_HOME/SOUL.md" 2>/dev/null || warn "SOUL.md not found in backup"
cp "$SCRIPT_DIR/.env" "$HERMES_HOME/.env" 2>/dev/null || warn ".env not found in backup"
mkdir -p "$HERMES_HOME/memories" && cp "$SCRIPT_DIR/memories/"*.md "$HERMES_HOME/memories/" 2>/dev/null

mkdir -p "$HERMES_HOME/skills"
if command -v rsync &>/dev/null; then rsync -a "$SCRIPT_DIR/skills/" "$HERMES_HOME/skills/"; else cp -r "$SCRIPT_DIR/skills/"* "$HERMES_HOME/skills/" 2>/dev/null; fi

mkdir -p "$HERMES_HOME/scripts"
if command -v rsync &>/dev/null; then rsync -a "$SCRIPT_DIR/scripts/" "$HERMES_HOME/scripts/"; else cp -r "$SCRIPT_DIR/scripts/"* "$HERMES_HOME/scripts/" 2>/dev/null; fi
chmod +x "$HERMES_HOME/scripts/"*.sh 2>/dev/null

mkdir -p "$HERMES_HOME/cron" && cp "$SCRIPT_DIR/cron/jobs.json" "$HERMES_HOME/cron/" 2>/dev/null

mkdir -p "$HERMES_HOME/wiki"
if command -v rsync &>/dev/null; then rsync -a "$SCRIPT_DIR/wiki/" "$HERMES_HOME/wiki/"; else cp -r "$SCRIPT_DIR/wiki/"* "$HERMES_HOME/wiki/" 2>/dev/null; fi
ok "Config files restored"

# ── Hindsight ─────────────────────────────────────────────────────────────────
if [ "$SKIP_HINDSIGHT" = false ]; then
 info "Installing Hindsight..."
 if command -v hindsight &>/dev/null; then
 ok "Hindsight already installed"
 else
 HINDSIGHT_OK=false
 # PEP 668: Debian 12+ blocks pip install。用 pipx 或 --break-system-packages 或 venv
 # 优先 pipx（最干净），其次 --break-system-packages，最后 venv fallback
 if command -v pipx &>/dev/null; then
  if pipx install hindsight-memory; then
   ok "Hindsight installed via pipx"
   HINDSIGHT_OK=true
  fi
 fi
 if [ "$HINDSIGHT_OK" = false ]; then
  for pipcmd in "pip install --break-system-packages" "pip3 install --break-system-packages" "python3 -m pip install --break-system-packages"; do
   if $pipcmd hindsight-memory; then
    ok "Hindsight installed via: $pipcmd hindsight-memory"
    HINDSIGHT_OK=true
    break
   fi
  done
 fi
 if [ "$HINDSIGHT_OK" = false ]; then
  # venv fallback
  warn "All pip methods failed. Trying venv fallback..."
  python3 -m venv "$HOME/.hindsight-venv" && \
  "$HOME/.hindsight-venv/bin/pip" install hindsight-memory && \
  ln -sf "$HOME/.hindsight-venv/bin/hindsight" "$LOCAL_BIN/hindsight" && \
  HINDSIGHT_OK=true && ok "Hindsight installed in ~/.hindsight-venv"
 fi
 if [ "$HINDSIGHT_OK" = false ]; then
  warn "Hindsight install failed. Manual options:"
  warn "  Option A: sudo apt install pipx && pipx install hindsight-memory"
  warn "  Option B: pip install --break-system-packages hindsight-memory"
  warn "  Option C: python3 -m venv ~/.hindsight-venv && ~/.hindsight-venv/bin/pip install hindsight-memory"
 fi
 fi
 mkdir -p "$HOME/.hindsight/profiles" && cp "$SCRIPT_DIR/hindsight/"* "$HOME/.hindsight/profiles/" 2>/dev/null
fi

# ── CC Switch + Claude Code ──────────────────────────────────────────────────
if [ "$SKIP_CC_SWITCH" = false ]; then
 info "Installing CC Switch + Claude Code..."

 # Check npm first
 if ! command -v npm &>/dev/null; then
 warn "npm not found. Installing Node.js..."
 if curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash - && sudo apt-get install -y nodejs; then
  ok "Node.js installed: $(node --version 2>/dev/null)"
 else
  warn "Node.js auto-install failed. Install manually: https://nodejs.org"
  warn "Then: npm i -g cc-switch @anthropic-ai/claude-code"
 fi
 fi

 if command -v npm &>/dev/null; then
 # npm global install 需要权限 — 用 sudo 或配 npm prefix
 NPM_PREFIX="$HOME/.npm-global"
 if ! command -v cc-switch &>/dev/null; then
  # 先试 sudo，不行就用 user prefix
  if npm install -g cc-switch 2>/dev/null; then
   ok "CC Switch installed"
  elif sudo npm install -g cc-switch 2>/dev/null; then
   ok "CC Switch installed (sudo)"
  else
   warn "CC Switch: npm package not found or permission denied"
   warn "cc-switch 可能已更名或需要从 GitHub 安装，跳过（非必须）"
  fi
 fi
 if ! command -v claude &>/dev/null; then
  if npm install -g @anthropic-ai/claude-code 2>/dev/null; then
   ok "Claude Code installed"
  elif sudo npm install -g @anthropic-ai/claude-code 2>/dev/null; then
   ok "Claude Code installed (sudo)"
  else
   warn "Claude Code install failed. Try: sudo npm i -g @anthropic-ai/claude-code"
  fi
 fi
 else
 warn "npm unavailable, skipping CC Switch + Claude Code. Install Node.js first."
 fi

 mkdir -p "$HOME/.cc-switch" && cp "$SCRIPT_DIR/cc-switch/"* "$HOME/.cc-switch/" 2>/dev/null
 mkdir -p "$HOME/.claude" && cp "$SCRIPT_DIR/claude/"* "$HOME/.claude/" 2>/dev/null
fi

# ── Interactive key setup ────────────────────────────────────────────────────
info ""
info "=========================================="
info " API Key Configuration"
info "=========================================="
info ""
info "Press Enter to skip any key (fill in later by editing ~/.hermes/.env)"

read -rp "OpenRouter API Key [sk-or-...]: " v; [ -n "$v" ] && sed -i "s|^OPENROUTER_API_KEY=.*|OPENROUTER_API_KEY=$v|" "$HERMES_HOME/.env"
read -rp "DeepSeek API Key [sk-...]: " v; [ -n "$v" ] && { sed -i "s|^DEEPSEEK_API_KEY=.*|DEEPSEEK_API_KEY=$v|" "$HERMES_HOME/.env"; sed -i "s|^HINDSIGHT_API_LLM_API_KEY=.*|HINDSIGHT_API_LLM_API_KEY=$v|" "$HOME/.hindsight/profiles/hermes.env" 2>/dev/null; }
read -rp "Default model API key for config.yaml: " v
if [ -n "$v" ]; then
 python3 -c "import yaml; f=open('$HERMES_HOME/config.yaml'); c=yaml.safe_load(f); c['model']['api_key']='$v'; open('$HERMES_HOME/config.yaml','w').write(yaml.dump(c,default_flow_style=False))" 2>/dev/null || warn "yaml edit failed, edit config.yaml manually"
fi
read -rp "Tavily API Key [tvly-...]: " v; [ -n "$v" ] && sed -i "s|^TAVILY_API_KEY=.*|TAVILY_API_KEY=$v|" "$HERMES_HOME/.env"
read -rp "Feishu App ID: " v; [ -n "$v" ] && sed -i "s|^# *FEISHU_APP_ID=.*|FEISHU_APP_ID=$v|" "$HERMES_HOME/.env"
read -rp "Feishu App Secret: " v; [ -n "$v" ] && sed -i "s|^# *FEISHU_APP_SECRET=.*|FEISHU_APP_SECRET=$v|" "$HERMES_HOME/.env"
read -rp "WeChat Account ID: " v; [ -n "$v" ] && sed -i "s|^# *WEIXIN_ACCOUNT_ID=.*|WEIXIN_ACCOUNT_ID=$v|" "$HERMES_HOME/.env"
read -rp "WeChat Token: " v; [ -n "$v" ] && sed -i "s|^# *WEIXIN_TOKEN=.*|WEIXIN_TOKEN=$v|" "$HERMES_HOME/.env"
read -rp "GitHub Token: " v
if [ -n "$v" ]; then
 if ! grep -q "GITHUB_TOKEN" "$HOME/.bashrc" 2>/dev/null; then
  echo "export GITHUB_TOKEN=$v" >> "$HOME/.bashrc"
 else
  sed -i "s|export GITHUB_TOKEN=.*|export GITHUB_TOKEN=$v|" "$HOME/.bashrc"
 fi
fi
read -rp "CC Switch AUTH_TOKEN: " v; [ -n "$v" ] && sed -i "s|export ANTHROPIC_AUTH_TOKEN=.*|export ANTHROPIC_AUTH_TOKEN=$v|" "$HOME/.cc-switch/env.sh" 2>/dev/null

# ── Set permissions ───────────────────────────────────────────────────────────
chmod 600 "$HERMES_HOME/.env" "$HERMES_HOME/config.yaml" 2>/dev/null

# ── Final diagnosis ───────────────────────────────────────────────────────────
echo ""
ok "=========================================="
ok " Setup Complete — Diagnosis:"
ok "=========================================="
echo ""

ISSUES=0

if command -v hermes &>/dev/null; then
 ok "hermes: $(hermes --version 2>/dev/null || echo 'installed')"
else
 # 再次尝试修复symlink
 if [ -f "$HERMES_BIN_IN_VENV" ]; then
  mkdir -p "$LOCAL_BIN"
  ln -sf "$HERMES_BIN_IN_VENV" "$LOCAL_BIN/hermes"
  if command -v hermes &>/dev/null; then
   ok "hermes: symlink fixed! $(hermes --version 2>/dev/null)"
  else
   err "hermes: symlink created but still not found — PATH issue"
   err "  Run: source ~/.bashrc"
   err "  Then: hermes --version"
   ISSUES=$((ISSUES+1))
  fi
 else
  err "hermes: NOT FOUND (venv binary missing)"
  err "  Re-run: bash $0 (without --skip-hermes)"
  ISSUES=$((ISSUES+1))
 fi
fi

if command -v hindsight &>/dev/null; then
 ok "hindsight: installed"
else
 warn "hindsight: not installed (optional)"
fi

if command -v cc-switch &>/dev/null; then
 ok "cc-switch: installed"
else
 warn "cc-switch: not installed (optional)"
fi

if command -v claude &>/dev/null; then
 ok "claude: installed"
else
 warn "claude: not installed (optional)"
fi

if [ -f "$HERMES_HOME/.env" ]; then
 ok "config: ~/.hermes/.env exists"
else
 warn "config: ~/.hermes/.env missing"
fi

echo ""
if [ $ISSUES -gt 0 ]; then
 warn "Issues found ($ISSUES)."
else
 ok "All core components ready!"
fi

# ── 一键激活 ────────────────────────────────────────────────────────────────
# bash 脚本是子进程，source ~/.bashrc 只影响子shell
# 最简方案：让用户用 source 而非 bash 执行脚本，这样脚本内的 export 直接生效
# 如果用户用了 bash 执行，给出一条命令刷新

if [ -f "$HERMES_BIN_IN_VENV" ]; then
 mkdir -p "$LOCAL_BIN"
 ln -sf "$HERMES_BIN_IN_VENV" "$LOCAL_BIN/hermes"
fi

# 在脚本内验证（PATH已在脚本开头export过了）
if command -v hermes &>/dev/null; then
 echo ""
 ok "验证: $(hermes --version 2>/dev/null || echo 'hermes found')"
 echo ""
 ok "下一步: hermes gateway run"
else
 echo ""
 warn "hermes 在当前脚本环境内不可用，你的终端需要刷新 PATH。"
 warn "执行这条命令（复制粘贴）："
 echo ""
 echo "  source ~/.bashrc && hermes --version"
 echo ""
fi
