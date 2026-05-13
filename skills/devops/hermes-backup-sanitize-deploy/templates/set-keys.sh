#!/usr/bin/env bash
# Quick API Key Update — no reinstall
set -euo pipefail
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC} $*"; }
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }

set_key() {
    local file="$1" key="$2" value="$3"
    if grep -q "^#*${key}=" "$file"; then
        sed -i "s|^#*${key}=.*|${key}=${value}|" "$file"
    elif grep -q "^${key}=" "$file"; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$file"
    else
        echo "${key}=${value}" >> "$file"
    fi
}

MODE="${1:-all}"
case "$MODE" in
    --llm-only) MODE="llm" ;; --messaging-only) MODE="messaging" ;; *) MODE="all" ;;
esac

[ "$MODE" = "all" ] || [ "$MODE" = "llm" ] && {
    info "=== LLM Keys ==="
    read -rp "OpenRouter API Key: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "OPENROUTER_API_KEY" "$v"
    read -rp "DeepSeek API Key: " v; [ -n "$v" ] && { set_key "$HERMES_HOME/.env" "DEEPSEEK_API_KEY" "$v"; set_key "$HOME/.hindsight/profiles/hermes.env" "HINDSIGHT_API_LLM_API_KEY" "$v"; }
    read -rp "Default model API key (config.yaml): " v; [ -n "$v" ] && python3 -c "import yaml; f=open('$HERMES_HOME/config.yaml'); c=yaml.safe_load(f); c['model']['api_key']='$v'; open('$HERMES_HOME/config.yaml','w').write(yaml.dump(c,default_flow_style=False))" 2>/dev/null || true
}

[ "$MODE" = "all" ] && {
    info "=== Utility Keys ==="
    read -rp "Tavily API Key: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "TAVILY_API_KEY" "$v"
    read -rp "GitHub Token: " v; [ -n "$v" ] && { grep -q "GITHUB_TOKEN" ~/.bashrc && sed -i "s|export GITHUB_TOKEN=.*|export GITHUB_TOKEN=$v|" ~/.bashrc || echo "export GITHUB_TOKEN=$v" >> ~/.bashrc; }
}

([ "$MODE" = "all" ] || [ "$MODE" = "messaging" ]) && {
    info "=== Messaging Keys ==="
    read -rp "Feishu App ID: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "FEISHU_APP_ID" "$v"
    read -rp "Feishu App Secret: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "FEISHU_APP_SECRET" "$v"
    read -rp "WeChat Account ID: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "WEIXIN_ACCOUNT_ID" "$v"
    read -rp "WeChat Token: " v; [ -n "$v" ] && set_key "$HERMES_HOME/.env" "WEIXIN_TOKEN" "$v"
}

chmod 600 "$HERMES_HOME/.env" 2>/dev/null || true
ok "Keys updated. Restart Hermes to apply."
