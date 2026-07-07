# Dify 变压器自动填报系统 — 工作流设计参考

## 项目概述

基于 Dify 工作流，输入变压器名称，自动从电力单线图中识别「变电站 + 10kV线路 + 杆塔号 + 变压器名称」完整路径，联网查询相关资料，完成自动填报。

## 核心架构

```
Start(输入: transformer_name + single_line_image)
  → LLM节点1 (Qwen2.5-VL, 多模态识别) → 输出: nodes+edges JSON
  → Code节点1 (Python, 路径回溯) → 输出: {substation, line_10kv, pole, transformer}
  → HTTP Request节点 (联网检索) → 输出: 容量/投运时间/所属单位
  → LLM节点2 (DeepSeek, 数据整合) → 输出: 结构化填报JSON
  → End节点 (输出结果 + 人工审核标记)
```

## 关键节点配置

### 多模态识别（LLM节点）

- **模型**: Qwen2.5-VL-72B（SiliconFlow API）
- **输入**: 图像 + 提示词
- **输出**: 设备节点列表 + 连接关系JSON（严格JSON格式）
- **提示词要点**: 电力符号命名规范（变电站="XX变"/"XX变电站"，线路="XX线"，杆塔="XX#杆"/"TXX"，变压器="XX变"/"T"）

### 路径回溯（Code节点）

- **Dify Code 节点使用 `inputs` 而非 `args` 接收上游输出**
- BFS向上回溯算法，构建反向邻接表
- 需处理边界条件：环检测、空路径、多路径

### 联网检索（HTTP Request节点）

- **方案A**: 调用电力行业公开API
- **方案B**: Dify内置搜索引擎 + LLM提取（兜底）

### 数据整合（LLM节点）

- **模型**: DeepSeek-V3（结构化输出能力强，成本低）
- **输出**: JSON格式填报数据，含置信度字段和需人工确认列表

## 验证结论

| 验证项 | 结论 |
|--------|------|
| Dify多模态工作流 | ✅ 可行（Dify 1.x+ 支持多模态LLM节点） |
| Dify Code节点 | ✅ 可行（Python代码节点） |
| Dify HTTP Request节点 | ✅ 可行 |
| Dify搜索工具 | ✅ 可行 |
| Qwen2.5-VL接入Dify | ✅ 可行（SiliconFlow OpenAI兼容API） |
| DeepSeek接入Dify | ✅ 可行 |

## 风险与应对

| 风险 | 等级 | 应对 |
|------|------|------|
| 单线图识别精度不足 | **高** | 提示词迭代 + few-shot示例 + 人工审核 + 置信度阈值(<0.8) |
| 变电站名称模糊匹配 | **中** | 名称归一化（去掉"变"/"变电站"后缀统一匹配） |
| Code节点超时 | **低** | 算法控制在500行以内 |

## 实施Phase

- **Phase 1** (1-2天): Dify工作流搭建 + 模型接入 + 测试验证
- **Phase 2** (0.5天): 表单输出节点 + 导出功能
- **Phase 3** (1-2天): 精度优化 + 人工审核 + API化

## 方案文档

完整方案文档: `.hermes/plans/2026-05-11-dify-transformer-filling-system-report.md`
