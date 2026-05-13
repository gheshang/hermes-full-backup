# Dify 工作流开发参考

> 来源：2026-05-11 变压器自动填报系统方案设计会话

## 节点类型与配置

### LLM 节点（多模态）

- **开启方式**：在 LLM 节点设置中开启"多模态"开关
- **输入变量**：文件类型变量需设为 `file` 而非 `text`，通过 `sys.files` 传递
- **模型要求**：必须选择支持视觉的模型（如 Qwen2.5-VL、GPT-4V、Claude 3.x）
- **提示词**：需明确要求输出结构化 JSON，避免自由文本

### Code 节点

- **变量接收**：使用 `inputs.get("key")` 而非 `args.get("key")`
- **超时限制**：建议控制在 500 行代码以内，复杂算法可能超时
- **支持语言**：Python（Dify 内置）

### HTTP Request 节点

- **原生支持**：可配置 URL、Method、Headers、Body
- **用途**：调用外部 API（如电力行业数据 API）
- **备选**：Dify 内置搜索工具节点（Google/Bing/自定义搜索）

### Start/End 节点

- **Start**：定义输入变量类型（text、file、number 等）
- **End**：定义输出格式（JSON、文本、文件下载链接）

## 关键陷阱

| 陷阱 | 表现 | 修复 |
|------|------|------|
| Code 节点变量名 | 用 `args.get()` 导致返回空值 | 改用 `inputs.get()` |
| 多模态未开启 | 图像输入被忽略，只处理文本 | 在 LLM 节点设置中手动开启"多模态"开关 |
| 文件变量类型 | 文件变量设为 `text` 类型 | 改为 `file` 类型 |
| 电力符号识别 | 通用 VLM 对电力专用符号识别率仅 60-70% | Few-shot 示例 + 置信度阈值 + 人工审核兜底 |

## 模型接入

### SiliconFlow (Qwen2.5-VL)

```
Base URL: https://api.siliconflow.cn/v1
API Key: 注册 https://cloud.siliconflow.cn 获取
模型名: Qwen/Qwen2.5-VL-72B-Instruct
```

### DeepSeek

```
Base URL: https://api.deepseek.com/v1
API Key: 注册 https://platform.deepseek.com 获取
模型名: deepseek-chat (V3) 或 deepseek-reasoner (R1)
```

## 工作流设计模式

### 多模态识别 → 结构化解析 → 业务逻辑 → 输出

```
Start (输入: 图像 + 文本)
  → LLM (多模态识别，输出 JSON)
  → Code (业务逻辑处理)
  → HTTP/搜索 (外部数据检索)
  → LLM (数据整合)
  → End (结构化输出)
```

### 置信度过滤模式

```
LLM 输出含 confidence 字段
  → Code 节点判断 confidence < 阈值
  → 低置信度字段标记"需人工确认"
  → End 输出含人工审核标记
```

## 验证检查清单

- [ ] Dify 版本是否支持多模态节点（1.x+）
- [ ] Code 节点使用 `inputs` 而非 `args`
- [ ] 文件输入变量类型设为 `file`
- [ ] LLM 节点已开启多模态开关
- [ ] 模型 API Key 已正确配置
- [ ] 提示词要求严格 JSON 输出
- [ ] 置信度阈值和人工审核环节已配置
