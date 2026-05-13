# Hindsight Daemon 启动失败 — 完整故障日志与修复

## 故障场景

Hermes Gateway 运行中，但 Hindsight retain 操作持续失败，日志中反复出现：

```
RuntimeError: Failed to start daemon for profile 'hermes'
RuntimeError: Cannot use HindsightEmbedded after it has been closed
WARNING plugins.memory.hindsight: Hindsight retain failed: Failed to start daemon for profile 'hermes'
```

同时伴随 API 认证错误：
```
Error code: 401 - {'error': {'message': 'Invalid token. If this should be a DS2API key, add it to ***.keys first.'}
```

## 根因

1. **HindsightEmbedded 数据库损坏** — 嵌入模式进程异常退出后，数据库文件处于不一致状态
2. **`.env` 中 `API_SERVER_KEY` 缺失** — 用户用 `cat >>` 追加而非 `cat >` 覆盖，导致配置不完整
3. **锁文件残留** — 异常退出后 `.lock` 文件未清理，阻止新进程启动

## 修复流程

```bash
# 1. 停止 gateway
systemctl --user stop hermes-gateway.service
sleep 5

# 2. 清理 hindsight 数据库和锁文件
rm -rf ~/.hermes/hindsight/*
rm -f ~/.hermes/*.lock ~/.cache/hermes/*.lock

# 3. 用覆盖模式重写 .env（关键：用 > 不是 >>）
PASS=$(openssl rand -base64 32 | tr -d '\n')
cat > ~/.hermes/.env << EOF
API_SERVER_ENABLED=true
API_SERVER_PORT=8642
API_SERVER_KEY=$PASS
EOF

# 4. 验证 .env 内容完整
cat ~/.hermes/.env
# 必须显示三行，API_SERVER_KEY 有值

# 5. 重启 gateway
systemctl --user start hermes-gateway.service
sleep 5

# 6. 验证
hermes gateway status
journalctl --user -u hermes-gateway.service -n 30 --no-pager
```

## 验证清单

| 检查项 | 预期结果 |
|--------|----------|
| `cat ~/.hermes/.env` | 三行配置完整，`API_SERVER_KEY` 有 32+ 字符值 |
| `hermes gateway status` | `active (running)`，无 RuntimeError |
| `journalctl ... -n 30` | 无 `Failed to start daemon` 和 `401` 错误 |
| `hermes memory test` | retain/recall 操作成功 |

## 常见错误

### 错误 1：用 `cat >>` 追加配置

```bash
# ❌ 错误
cat >> ~/.hermes/.env << 'EOF'
API_SERVER_KEY=生成一个强密码
EOF
```

结果：`.env` 中可能有多行重复配置，或 `API_SERVER_KEY` 被注释掉/覆盖。

### 错误 2：密码为空或格式错误

```bash
# ❌ 错误 — 密码为空
API_SERVER_KEY=

# ❌ 错误 — 密码包含换行
API_SERVER_KEY=$(echo -e "password\n")
```

### 错误 3：清理后不验证 .env

修复 hindsight 数据库后，如果 `.env` 仍然缺失 `API_SERVER_KEY`，daemon 会因为认证失败再次启动失败。

## 关联问题

- 磁盘空间不足 → hindsight 数据库文件损坏
- `.env` 配置缺失 → API 认证失败 → daemon 启动失败
- 锁文件残留 → 新进程无法启动
