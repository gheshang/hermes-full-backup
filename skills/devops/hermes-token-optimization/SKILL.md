---
name: hermes-token-optimization
description: Interactive guide script for optimizing Hermes Agent token consumption via compression, auxiliary models, search backend, and memory system configuration.
version: 3.2
author: 上河一号
metadata:
  hermes:
    tags: [hermes, token, compression, auxiliary, cost-optimization, search, memory]
    related_skills: [karpathy-coding-guidelines, agency-agents-zh, hermes-config-setup]
---

# Hermes Agent 全量配置引导

## 触发条件
用户要求节省 Hermes token 消耗，配置 compression / auxiliary / 搜索 / 记忆系统。

## 核心原理
让便宜的小模型在后台做上下文压缩总结，主模型只处理精简后的内容，大幅降低计费。

## 与 hermes-config-setup 的关系
`hermes-config-setup` 是脚本级配置指南（含安全陷阱、代码审查流程）。
本 skill 是配置参数级指南（含压缩参数、成本计算）。
两者互补：本 skill 决定"配什么"，hermes-config-setup 决定"怎么安全地写脚本配"。

## 审查流程（写完代码必走，两步缺一不可）

### 第一步：能否跑通（语法/运行时）
- `ast.parse` 检查语法
- 未使用 import 扫描
- 函数/变量引用完整性（调用的函数是否都已定义）
- 类型/边界校验

### 第二步：能否达成目标（功能逻辑闭环）
- 每个配置项的输入链是否完整：用户需要提供的信息（provider/model/base_url/api_key）是否都有入口？
- 输出链是否闭环：config.yaml 写了字段，但 .env 里的凭证是否也引导写入了？
- 缺失任何一个输入 = 配置写了但跑不起来 = 白写
- 用"用户跑完这个功能，最终效果能不能生效"的视角逐项验证

### 第三步：角色审查 — agency-agents-zh 角色库
- 代码审查员 (`engineering/engineering-code-reviewer.md`) — 🔴阻塞/🟡建议/💭小改进
- 安全工程师 (`engineering/engineering-security-engineer.md`) — 对抗性思维：什么可被滥用？失败时发生什么？爆炸半径多大？

### 第四步：Karpathy 元规则走查 (`karpathy-coding-guidelines`)
- 简洁优先：200行能50行就重写
- 精准修改：每行改动必须追溯到用户请求
- 目标驱动执行：每步有验证标准

流程：第一步+第二步 → skill_view(name="agency-agents-zh") → read_file 读角色 md → 按角色规则审查 → 修完再过 → 直到零 🔴 阻塞项

## 配置范围（四层 10 项）

### 第一层：密钥池策略
| 配置项 | 作用 | 推荐值 |
|--------|------|--------|
| credential_pool_strategies.{provider} | 避免单密钥耗尽中断任务 | least_used |

需配合 `hermes auth add` 添加多个密钥。

### 第二层：Context 压缩
| 配置项 | 作用 | 推荐值 |
|--------|------|--------|
| model.context_length | 按模型真实窗口设置 | GLM-5=200000 |
| model.max_tokens | 避免输出截断 | GLM-5=131072 |
| compression.threshold | 何时触发压缩 | 0.75 |
| compression.target_ratio | 压缩后保留比例 | 0.25 |
| compression.protect_last_n | 保护最近N条消息 | 30 |
| compression.summary_model | 用便宜模型做压缩总结 | glm-4-flash |
| compression.enabled | 压缩开关 | true |

### 第三层：Auxiliary 模型
重任务（需理解力）：vision, web_extract, flush_memories
轻任务（纯分类/搜索）：compression, session_search, approval, skills_hub, mcp

### 第四层：Smart Model Routing（v0.10.0 不支持）
知乎文章提到的 `smart_model_routing` 在 Hermes v0.10.0 中 **不存在此配置项**。
`hermes config set` 会写入但不报错，运行时直接忽略。
等效方案：通过 auxiliary 副驾系统（第三层）将轻任务指向便宜模型。

**教训：写脚本前必须验证配置项是否真实存在于 Hermes DEFAULT_CONFIG 中。**
验证方法：`from hermes_cli.config import DEFAULT_CONFIG; print(list(DEFAULT_CONFIG.keys()))`

每个副驾需配：
- auxiliary.{task}.provider — 厂商
- auxiliary.{task}.model — 模型名
- auxiliary.{task}.base_url — 自定义厂商必填
- auxiliary.{task}.api_key_env — .env 中的变量名
- 密钥写入 .env（权限 0600），不写 config.yaml

## 双压缩系统（官方文档 2026-04-24 确认）

Hermes 有**两层独立压缩**，不要混淆：

| 层 | 位置 | 触发阈值 | 作用 |
|---|------|---------|------|
| Gateway Session Hygiene | `gateway/run.py` | 固定 85% | 安全网，防长会话溢出 |
| Agent ContextCompressor | `agent/context_compressor.py` | 可配（默认 50%） | 正常上下文管理 |

设置 compression.threshold 时注意：0.50 是官方默认，0.75 是知乎建议值。设太高（>0.85）会导致 Gateway 安全网先触发，质量更差。

## context.engine 可替换（官方文档确认）

```yaml
context:
  engine: "compressor"  # 默认 — 有损摘要压缩
  engine: "lcm"         # LCM 插件 — 无损上下文管理
```

插件引擎需用户显式设置 `context.engine` 才会激活，不会自动替换。
安装方式：`hermes plugins` → Provider Plugins → Context Engine，或直接编辑 config.yaml。

## 关键陷阱

### 1. 配置项不存在
`hermes config set` 什么都能写，不存在的 key 也不报错，但运行时直接忽略。
写脚本前必须验证：`from hermes_cli.config import DEFAULT_CONFIG` 检查 key 是否存在。

### 2. custom 厂商四件套缺一不可
自定义厂商（custom）必须同时设置 provider + model + base_url + api_key，缺一不可。
只填 provider 和 model 而不填 base_url 和 api_key，副驾不会生效，会 fallback 到主模型，反而更费 token。

### 3. write_env 必须保留 .env 原有内容
写入 .env 时必须行级更新（按 key 替换或追加），不能只写键值对——否则会删掉所有注释、空行和未涉及的 key。
正确做法：逐行读取 → 找到同 key 的行号 → 替换该行 → 末尾追加新 key → 写回全文。

### 4. 凭证安全
API key 存 .env 权限 0600，不写 config.yaml。

脚本中凡是引导用户配置 custom 厂商的地方，必须同时引导输入 base_url 和 api_key，并写入 .env。
否则配置了但跑不起来 = 白配 = 比不配还差（因为给了用户"已优化"的错觉）。

## 合并说明
本 skill 已与 `hermes-config-setup` 合并为单一脚本 `~/.hermes/hermes_setup_all.py`。
Token 优化相关功能在该脚本的**第二层**（选项 4-7）：密钥池 / 上下文窗口 / 上下文压缩 / Token 监控。
**第三层（成本控制，v4.0 新增）**：Provider Routing(13) / Fallback Provider(14) / Shell Hooks(15) / Nous Tool Gateway(16)。
旧脚本 `~/.hermes/hermes_token_optimizer.py` 已删除。

## 官方文档新发现（已纳入脚本 v4.0）
- **双压缩系统**：Gateway 安全网 85% + Agent 主压缩 50%（可调），不是单层
- **context.engine 可替换**：默认 compressor（有损），可换 LCM（无损）等插件引擎
- **compression 默认值**：官方 threshold=0.50, target_ratio=0.20, protect_last_n=20（知乎建议值更高）
- **Provider Routing**：OpenRouter 下 sort=price 直接走最便宜通道
- **Fallback Provider**：跨 provider 自动故障切换，密钥池先试，全失败再 fallback

## 知乎文章出处
《Hermes Agent 成本优化大揭秘》— 四层联动：密钥池 + Context压缩 + Auxiliary模型 + Smart Routing，理论节省 81% 年度成本。
**注意**：第四层 Smart Routing 为文章理论构想，Hermes v0.10.0 尚不支持，等效方案为 auxiliary 副驾系统。
