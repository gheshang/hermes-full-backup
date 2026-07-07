# 路径拼写陷阱 — .herms/ vs .hermes/

## 问题描述

将 `~/.hermes/` 误写为 `~/.herms/` 会导致：
1. 文件写入成功但无法读取（目录不存在或为空）
2. 引发重复重试循环，直到系统主动阻断（通常 5-10 次后 BLOCKED）
3. 浪费大量 token 和时间

## 触发场景

- 手动拼写配置路径时
- 使用 `write_file` / `read_file` / `terminal` 命令时
- 任何涉及 `~/.hermes/` 路径的操作

## 预防措施

```bash
# 每次文件操作后验证路径
ls -la ~/.hermes/plans/
test -f ~/.hermes/plans/some-file.md && echo "OK" || echo "PATH ERROR"
```

## 修复步骤

```bash
# 1. 检查是否有误写的目录
ls -la ~/.herms/ 2>/dev/null && echo "Found typo dir — remove it"

# 2. 移动正确路径的文件
mv ~/.herms/plans/* ~/.hermes/plans/ 2>/dev/null

# 3. 删除错误目录
rm -rf ~/.herms/

# 4. 验证
ls ~/.hermes/plans/
```

## 教训

> 路径拼写错误是最高频的低级错误之一。每次涉及 `~/.hermes/` 的操作，写完后必须验证路径存在性。不要依赖系统自动纠错——它不存在。
