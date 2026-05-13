# Hindsight Memory Provider 模型配置缺失

## 问题描述

Hindsight 作为 memory provider 时，`config.yaml` 中仅配置了 `provider: hindsight`，但**缺少独立的模型配置**（model/base_url/api_key），导致 hindsight 无法调用 LLM 进行记忆提取和反思。

## 症状

- `RuntimeError: Failed to start daemon for profile 'hermes'`
- `WARNING plugins.memory.hindsight: Hindsight retain failed`
- 记忆功能部分或完全失效

## 根因

Hindsight plugin 在 `config.yaml` 中读取 memory 配置时，需要以下字段：

```yaml
memory:
  memory_enabled: true
  provider: hindsight
  # 以下字段不能为空：
  model: sensenova-6.7-flash-lite      # ← 必须指定
  provider: custom                      # ← 必须指定（与主模型一致）
  base_url: https://token.sensenova.cn/v1  # ← 必须指定
  api_key_env: MAIN_API_KEY             # ← 必须指定（引用 .env 中的 key）
```

如果只写 `provider: hindsight` 而无模型配置，hindsight 会使用空值，导致 daemon 启动失败。

## 修复步骤

1. 编辑 `~/.hermes/config.yaml`，在 `memory:` 下添加模型配置
2. `api_key_env` 应指向 `.env` 中定义的变量名（如 `MAIN_API_KEY`）
3. 重启 gateway：`systemctl --user restart hermes-gateway.service`
4. 验证：`hermes gateway status` + `journalctl ... -n 30`

## 与 hindsight-api 工具的关系

hindsight 的 daemon 模式（embedded）需要 `hindsight-api` 工具，该工具通过 UV 安装，占用约 **5.6G**（含 PyTorch + CUDA 栈）：

```
~/.local/share/uv/tools/hindsight-api/
├── lib/python3.11/site-packages/
│   ├── nvidia/          2.7G
│   ├── torch/           1.2G
│   └── triton/          640M
```

**如果 hindsight 使用远程模式（非 embedded），此工具可安全删除**，释放 5.6G。

判断方法：
```bash
grep -A 10 'memory:' ~/.hermes/config.yaml
# 如果只有 provider: hindsight 而无 mode: embedded，说明用的是远程模式
```

删除命令：
```bash
rm -rf ~/.local/share/uv/tools/hindsight-api
```

## 参考

- `hindsight-troubleshooting` skill — 完整排错链路
- `disk-space-audit-and-cleanup` skill — UV 工具清理
