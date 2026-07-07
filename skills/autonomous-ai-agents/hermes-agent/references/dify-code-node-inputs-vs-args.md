# Dify Code 节点 API 陷阱 — `inputs` vs `args`

## 问题描述

Dify 工作流中的 Code 节点（Python）接收上游节点输出的方式与常见 Python 函数签名不同：

- ❌ **错误写法**：`def main(args: dict) -> dict:` — 这是大多数 Python 函数的习惯写法
- ✅ **正确写法**：`def main(inputs: dict) -> dict:` — Dify Code 节点使用 `inputs` 作为参数名

## 触发场景

在 Dify 工作流中编写 Python Code 节点时，如果沿用常规 Python 函数的参数命名习惯，会导致：
- 上游节点的输出无法被 Code 节点接收
- `inputs.get("key")` 返回 `None`（因为实际参数是 `args`，但 Dify 传入的是 `inputs` 字典）
- 整个工作流数据传递中断

## 解决方案

```python
def main(inputs: dict) -> dict:
    """Dify Code 节点的正确签名"""
    nodes = inputs.get("nodes", [])
    edges = inputs.get("edges", [])
    target = inputs.get("target_transformer", "")
    # ...
```

## 验证方法

在 Dify 工作流中测试 Code 节点时：
1. 上游节点输出 JSON 数据
2. Code 节点打印 `inputs` 的内容确认接收
3. 如果输出为空或 `None`，检查参数名是否为 `inputs`

## 来源

2026-05-11 会话中发现：在编写 Dify 变压器填报系统的路径回溯 Code 节点时，最初使用 `args` 参数名，导致数据传递失败。通过验证发现 Dify 使用 `inputs`。
