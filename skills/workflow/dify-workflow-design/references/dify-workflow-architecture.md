# Dify 工作流架构参考

## 多模态工作流节点配置

### LLM节点开启多模态
1. 选择支持视觉的模型（Qwen2.5-VL、InternVL2等）
2. 在节点设置中开启"多模态"开关
3. 输入变量类型设为 `file` 而非 `text`
4. 系统提示词中明确说明"你将接收一张图片，请分析..."

### 文件变量传递
- 工作流输入变量类型：`file`（支持图片/PDF）
- 在LLM节点中通过 `sys.files` 访问上传的文件
- Dify会自动将文件转换为模型可接受的格式

## 节点间数据传递

### Code节点输入
- 上游节点输出通过 `inputs` 字典传递
- 使用 `inputs.get("变量名")` 而非 `args.get()`
- 示例：
  ```python
  nodes = inputs.get("nodes", [])
  edges = inputs.get("edges", [])
  ```

### 结构化输出
- LLM节点开启"JSON Schema"输出模式
- 在输出变量中配置JSON Schema
- 确保提示词中要求"严格JSON，不要其他文字"

## 联网检索方案

### 方案A：HTTP Request节点
- 直接调用外部API
- 需要API Key（在Dify中配置为环境变量）
- 适合有明确API接口的场景

### 方案B：Dify搜索工具
- 内置搜索引擎节点
- 可配置Google/Bing/自定义搜索
- 后续LLM节点从搜索结果中提取结构化信息
- 适合无明确API的场景

## 电力单线图识别提示词模板

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

## 路径回溯算法（Python）

```python
def main(args: dict) -> dict:
    """
    从变压器节点向上回溯，构建完整供电路径。
    输入: nodes, edges, target_transformer
    输出: {substation, line_10kv, pole, transformer}
    """
    import json
    from collections import defaultdict

    nodes = args.get("nodes", [])
    edges = args.get("edges", [])
    target = args.get("target_transformer", "")

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

## 已知风险与应对

| 风险 | 等级 | 应对 |
|------|------|------|
| 电力符号识别精度 | 高 | 提示词迭代+few-shot示例+置信度阈值过滤 |
| 变电站名称模糊匹配 | 中 | 名称归一化（去掉"变"/"变电站"后缀统一匹配） |
| 单线图非树状结构 | 中 | 回溯算法增加环检测、多路径输出 |
| Dify Code节点超时 | 低 | 控制在500行以内 |

## 模型推荐

| 用途 | 推荐模型 | 理由 |
|------|----------|------|
| 多模态识别 | Qwen2.5-VL-72B (SiliconFlow) | 中文电力术语理解好，API稳定 |
| 数据整合 | DeepSeek-V3 | 结构化输出能力强，成本低 |
| 备选多模态 | InternVL2-40B | 开源可本地部署 |
