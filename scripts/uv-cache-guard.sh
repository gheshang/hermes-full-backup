#!/usr/bin/env bash
# uv 缓存自动清理脚本
# 当缓存超过阈值时自动清理
# 阈值: 2GB（29G VPS 的合理上限）

set -euo pipefail

CACHE_DIR=$(uv cache dir 2>/dev/null || echo "$HOME/.cache/uv")
MAX_BYTES=$((2 * 1024 * 1024 * 1024))  # 2GB

# 获取缓存大小（字节）
if [ ! -d "$CACHE_DIR" ] || [ -z "$(ls -A "$CACHE_DIR" 2>/dev/null)" ]; then
    echo "uv cache is empty, nothing to do."
    exit 0
fi

CACHE_BYTES=$(du -sb "$CACHE_DIR" 2>/dev/null | awk '{print $1}')
CACHE_MB=$((CACHE_BYTES / 1024 / 1024))
MAX_MB=$((MAX_BYTES / 1024 / 1024))

echo "uv cache: ${CACHE_MB}MB / ${MAX_MB}MB limit"

if [ "$CACHE_BYTES" -gt "$MAX_BYTES" ]; then
    echo "Cache exceeds ${MAX_MB}MB limit, cleaning..."
    uv cache clean
    echo "Cache cleaned."
else
    echo "Cache within limit, pruning unreachable entries..."
    uv cache prune 2>/dev/null || true
    echo "Prune done."
fi
