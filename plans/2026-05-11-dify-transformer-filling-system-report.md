# Dify 变压器自动填报系统方案报告

> **目标：** 基于 Dify 工作流，输入变压器名称，自动从电力单线图中识别「变电站 + 10kV线路 + 杆塔号 + 变压器名称」完整路径，联网查询相关资料，完成自动填报。

---

## 一、需求拆解

### 核心流程

```
用户输入变压器名称
    ↓
[步骤1] 上传/提供对应电力单线图（图片/PDF）
    ↓
[步骤2] 多模态OCR识别 → 提取图中所有设备节点及连接关系
    ↓
[步骤3] 图结构解析 → 从变压器节点向上回溯，构建完整层级路径
    ↓
[步骤4] 联网检索 → 查询该变电站/线路的官方资料
    ↓
[步骤5] 结构化输出 → 生成标准填报表单（JSON/Excel/HTML）
    ↓
[步骤6] 人工审核 → 确认无误后提交
```

### 关键难点

| 难点 | 说明 | 解决思路 |
|------|------|----------|
| 单线图识别精度 | 电力单线图符号复杂（断路器、隔离开关等专用符号），通用OCR无法识别 | 多模态VLM（Qwen2.5-VL/InternVL2）+ 电力符号微调提示词 |
| 拓扑关系提取 | 图中设备用线条连接，需识别「谁连谁」的层级关系 | VLM输出结构化JSON（节点+边） |
| 路径回溯逻辑 | 从变压器向上找杆塔→线路→变电站，需理解电力系统命名规范 | Dify Code节点写回溯算法 |
| 联网检索准确性 | 变电站名称可能存在别名/简称，需模糊匹配 | Dify搜索工具或HTTP Request节点 |

---

## 二、Dify 工作流架构设计

### 2.1 节点拓扑

```
┌─────────────────────────────────────────────────────────────────┐
│                     Dify Workflow (Chatflow)                     │
├─────────────────────────────────────────────────────────────────┤
│  [Start]                                                        │
│   ├── 变量: transformer_name (文本)                              │
│   ├── 变量: single_line_image (文件上传)                         │
│   ▼                                                             │
│  [LLM节点1] Qwen2.5-VL → 多模态识别单线图                        │
│   输出: 设备节点列表 + 连接关系JSON                               │
│   ▼                                                             │
│  [Code节点1] Python → 路径回溯算法                                │
│   输出: {substation, line_10kv, pole, transformer}              │
│   ▼                                                             │
│  [HTTP Request节点] → 联网检索变电站/线路资料                      │
│   输出: 容量/投运时间/所属单位等                                  │
│   ▼                                                             │
│  [LLM节点2] DeepSeek → 数据整合 + 填报表单生成                     │
│   输出: 结构化填报JSON                                            │
│   ▼                                                             │
│  [End节点] → 输出填报结果 + 人工审核标记                           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 各节点详细配置

#### 节点1：多模态识别（LLM节点）

**模型选择：** Qwen2.5-VL-72B（硅基流动/SiliconFlow API，支持中文电力术语）

**系统提示词：**

```
你是一名电力工程师，负责从电力单线图中提取设备信息。

任务：分析上传的单线图，识别图中所有电力设备节点及其连接关系。

输出格式（严格JSON，不要其他文字）：
{
  "nodes": [
    {"id": "n1", "type": "substation|line|pole|transformer|breaker|isolator", "name": "设备名称/编号", "bbox": [x1,y1,x2,y2]},
    ...
  ],
  "edges": [
    {"from": "n1", "to": "n2", "relation": "connected|feeds|branches"},
    ...
  ],
  "transformer_found": "识别到的变压器名称",
  "confidence": 0.0-1.0
}

规则：
1. 变电站：通常标注为"XX变电站"或"XX变"
2. 10kV线路：标注为"XX线"或"10kV XX线"
3. 杆塔：标注为"XX#杆"或"TXX"
4. 变压器：标注为"XX变"或"变压器"或"T"
5. 连接关系按图中线条走向判断，从变电站→线路→杆塔→变压器为供电方向
```

#### 节点2：路径回溯（Code节点）

**Python代码：**

```python
def main(inputs: dict) -> dict:
    """
    从变压器节点向上回溯，构建完整供电路径。
    输入: nodes, edges, target_transformer
    输出: {substation, line_10kv, pole, transformer}
    """
    from collections import defaultdict

    nodes = inputs.get("nodes", [])
    edges = inputs.get("edges", [])
    target = inputs.get("target_transformer", "")

    # 构建反向邻接表（谁指向谁）
    reverse_adj = defaultdict(list)
    node_map = {n["id"]: n for n in nodes}

    for e in edges:
        reverse_adj[e["to"]].append(e["from"])

    # 找到目标变压器节点
    tx_node = None
    for n in nodes:
        if target.lower() in n.get("name", "").lower() or n.get("type") == "transformer":
            tx_node = n
            break

    if not tx_node:
        return {"error": f"未找到变压器: {target}"}

    # BFS向上回溯
    path = {"transformer": tx_node["name"], "pole": "", "line_10kv": "", "substation": ""}
    visited = {tx_node["id"]}
    current = tx_node["id"]

    while True:
        parents = reverse_adj.get(current, [])
        if not parents:
            break

        found_new = False
        for p_id in parents:
            if p_id in visited:
                continue
            visited.add(p_id)
            p_node = node_map.get(p_id)
            if not p_node:
                continue

            p_type = p_node.get("type", "")
            if p_type == "pole" and not path["pole"]:
                path["pole"] = p_node["name"]
            elif p_type == "line" and not path["line_10kv"]:
                path["line_10kv"] = p_node["name"]
            elif p_type == "substation" and not path["substation"]:
                path["substation"] = p_node["name"]

            current = p_id
            found_new = True

        if not found_new:
            break

    return path
```

> **注意：** Dify Code 节点使用 `inputs` 而非 `args` 接收上游输出。

#### 节点3：联网检索（HTTP Request节点）

**方案A（推荐）：调用电力行业公开API**

```
GET https://api.example.com/substation/query?name={substation_name}
Headers: Authorization: Bearer {API_KEY}
```

**方案B（兜底）：Dify内置搜索引擎 + LLM提取**

- 使用Dify的"搜索工具"节点，搜索 `{substation_name} 变电站 容量 投运`
- 后续LLM节点从搜索结果中提取结构化信息

#### 节点4：数据整合与填报（LLM节点）

**模型选择：** DeepSeek-V3（成本低，结构化输出能力强）

**系统提示词：**

```
根据以下信息生成标准电力设备填报表单：

供电路径：
- 变电站：{substation}
- 10kV线路：{line_10kv}
- 杆塔号：{pole}
- 变压器：{transformer}

检索到的补充信息：
{search_results}

请输出JSON格式填报数据：
{{
  "填报时间": "YYYY-MM-DD HH:MM",
  "供电路径": {{
    "变电站": "",
    "10kV线路": "",
    "杆塔号": "",
    "变压器名称": ""
  }},
  "设备参数": {{
    "变压器容量(kVA)": "",
    "投运日期": "",
    "所属供电局": "",
    "线路长度(km)": "",
    "杆塔类型": ""
  }},
  "数据来源": ["单线图识别", "联网检索"],
  "置信度": 0.0-1.0,
  "需人工确认": ["字段名1", "字段名2"]
}}

规则：
1. 置信度<0.8的字段必须加入"需人工确认"列表
2. 缺失数据留空字符串，不要编造
3. 时间格式统一为YYYY-MM-DD
```

---

## 三、技术选型

| 模块 | 推荐方案 | 备选方案 | 理由 |
|------|----------|----------|------|
| 多模态识别 | Qwen2.5-VL-72B (SiliconFlow) | InternVL2-40B | 中文电力术语理解好，API稳定 |
| 数据整合LLM | DeepSeek-V3 | Qwen2.5-72B-Instruct | 结构化输出能力强，成本低 |
| 联网检索 | Dify搜索工具 + LLM | 自定义HTTP节点调用电力API | 快速上线用搜索，后期可替换为专业API |
| 部署方式 | Dify Cloud / 私有Docker部署 | — | 根据数据敏感度选择 |

---

## 四、实施步骤

### Phase 1：Dify工作流搭建（1-2天）

1. **注册/部署Dify**
   - 使用Dify Cloud（https://cloud.dify.ai）快速验证
   - 或 Docker私有部署：`docker-compose up -d`

2. **配置模型接入**
   - SiliconFlow API（Qwen2.5-VL）：注册获取API Key，在Dify模型管理中添加
   - DeepSeek API：同上

3. **创建工作流（Workflow模式）**
   - 添加Start节点，定义输入变量：`transformer_name`（文本）、`single_line_image`（文件）
   - 添加LLM节点1（多模态识别），配置Qwen2.5-VL模型和提示词
   - 添加Code节点1（路径回溯），粘贴Python代码
   - 添加HTTP Request节点或搜索工具节点（联网检索）
   - 添加LLM节点2（数据整合），配置DeepSeek模型和提示词
   - 添加End节点，输出结构化JSON

4. **测试验证**
   - 上传一张电力单线图测试样本
   - 输入变压器名称，检查全流程输出
   - 调整提示词和代码逻辑，迭代优化识别精度

### Phase 2：填报表单输出（0.5天）

5. **添加表单输出节点**
   - 在End节点前添加一个LLM节点，将JSON转为HTML表单或Markdown表格
   - 或使用Dify的"模板"功能生成预定义格式的填报单

6. **导出功能**
   - 配置工作流输出为可下载的文件（JSON/CSV/HTML）
   - 或通过HTTP Request节点将数据推送到填报系统API

### Phase 3：优化与生产化（1-2天）

7. **提升识别精度**
   - 收集更多电力单线图样本，优化提示词
   - 考虑微调Qwen2.5-VL（如果有足够标注数据）
   - 添加后处理校验规则（如：变压器名称必须符合命名规范）

8. **添加人工审核环节**
   - 在End节点前添加"人工审核"标记
   - 置信度<0.8的字段高亮显示
   - 支持用户手动修正后重新提交

9. **API化**
   - 获取Dify工作流的API Endpoint
   - 编写Python/Node.js客户端，封装为内部服务
   - 支持批量处理（传入多个变压器名称）

---

## 五、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| 单线图识别精度不足 | 路径回溯错误，填报数据错误 | ① 提示词迭代优化 ② 添加人工审核环节 ③ 置信度阈值过滤 |
| 联网检索无结果 | 补充信息缺失 | ① 多源检索（搜索引擎+行业数据库）② 允许空值，标记需人工补充 |
| Dify工作流复杂度高 | 调试周期长 | ① 先做最小可用版本（MVP）② 分节点独立测试 |
| 数据隐私问题 | 单线图含敏感信息 | 私有Docker部署，不上传公有云 |

---

## 六、MVP最小可行方案

如果时间紧迫，优先实现以下核心链路：

```
输入变压器名称 + 单线图
    → Qwen2.5-VL识别（提取节点+边）
    → Code节点回溯路径
    → DeepSeek生成填报JSON
    → 输出（人工审核）
```

**跳过项：** 联网检索（Phase 2补）、批量处理（Phase 3补）、API封装（Phase 3补）

---

## 七、验证结果

子agent验证结论：

### ✅ 可行的部分

| 验证项 | 结论 | 依据 |
|--------|------|------|
| Dify多模态工作流 | **可行** | Dify 1.x+ 支持在LLM节点中开启"多模态"选项，接收图像输入；文件变量通过 `sys.files` 传递 |
| Dify Code节点 | **可行** | Dify Workflow支持Python代码节点，可执行路径回溯逻辑 |
| Dify HTTP Request节点 | **可行** | 原生支持，可调用外部API |
| Dify搜索工具 | **可行** | 内置搜索引擎节点，可配置Google/Bing/自定义搜索 |
| Qwen2.5-VL接入Dify | **可行** | SiliconFlow提供OpenAI兼容API，Dify支持自定义OpenAI兼容模型接入 |
| DeepSeek接入Dify | **可行** | DeepSeek提供OpenAI兼容API，Dify已内置支持 |

### ⚠️ 需要调整的部分

| 问题 | 原方案 | 调整后 |
|------|--------|--------|
| **Code节点变量传递** | 使用 `args.get()` | Dify Code节点使用 `inputs.get()` 接收上游输出（已在代码中修正） |
| **电力符号识别精度** | 依赖通用VLM提示词 | 通用VLM对电力专用符号识别率约60-70%，需：①收集样本微调提示词 ②添加后处理校验规则 ③置信度<0.7强制人工审核 |
| **路径回溯边界条件** | 假设图为树状结构 | 实际单线图可能有环/分支，需补充：①检测环并报错 ②多路径时输出所有可能路径 |

### 🔴 风险项

| 风险 | 等级 | 说明 |
|------|------|------|
| 单线图识别精度 | **高** | 电力单线图符号高度专业化，通用VLM无法准确识别断路器、隔离开关等符号，可能导致拓扑关系错误 |
| 变电站名称模糊匹配 | **中** | 联网检索时，"XX变"与"XX变电站"可能匹配不到同一实体，需做名称归一化 |
| Dify Code节点超时 | **低** | 复杂回溯算法可能超时，建议控制在500行以内 |

### 📋 方案调整建议

1. **MVP阶段增加人工审核节点**：在End节点前强制添加人工确认环节，置信度<0.8的字段必须人工复核
2. **Code节点增加异常处理**：添加环检测、空路径检测、多路径输出
3. **联网检索增加名称归一化**：在检索前对变电站名称做标准化（去掉"变"/"变电站"后缀统一匹配）
4. **提示词增加few-shot示例**：在VLM提示词中加入3-5个电力单线图示例，提升识别精度

**总体结论：方案架构可行，核心链路（多模态识别→路径回溯→联网检索→结构化输出）在Dify上可完整实现。最大风险是单线图识别精度，需通过提示词优化+人工审核环节兜底。**

---

## 八、后续扩展方向

1. **多语言支持**：支持英文/日文电力单线图识别
2. **CAD图纸直接解析**：集成DWG/DXF解析，跳过图片OCR
3. **历史数据关联**：接入电力GIS系统，自动填充设备参数
4. **异常检测**：识别单线图中的异常连接或设备缺失
5. **语音交互**：通过Dify的语音节点支持语音输入变压器名称

---

## 九、环境准备清单

| 项 | 状态 | 操作 |
|---|---|---|
| Dify 账号 | ❓ | 注册 https://cloud.dify.ai 或私有部署 |
| DeepSeek API Key | ✅ | 已在 `.env` 中 |
| SiliconFlow API Key | ❌ | 需注册 https://cloud.siliconflow.cn 获取 |
| 电力单线图测试样本 | ❓ | 需提供至少1张测试图片 |
| Dify 工作流 API Token | ❓ | 创建工作流后在"API访问"中获取 |

---

**方案文件路径：** `.hermes/plans/2026-05-11-dify-transformer-filling-system.md`
