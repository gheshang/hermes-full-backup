---
name: dify-workflow-design
description: 设计Dify工作流用于自动化数据填报、多模态识别、联网检索等场景。涵盖节点配置、数据传递、提示词模板、风险应对。
version: 1.0.0
author: 上河一号
metadata:
  hermes:
    tags: [dify, workflow, automation, multi-modal, low-code]
---

# Dify 工作流设计指南

## 适用场景

- 多模态识别（图像/文档→结构化数据）
- 自动化数据填报（从非结构化输入生成标准表单）
- 联网检索+数据整合（搜索+LLM提取）
- 工业/电力/医疗等专业领域自动化

## 核心节点配置

### 多模态LLM节点
1. 选择支持视觉的模型（Qwen2.5-VL、InternVL2等）
2. 开启"多模态"开关
3. 输入变量类型设为 `file`
4. 提示词明确说明接收图片

### Code节点
- 上游输出通过 `inputs` 字典传递
- 使用 `inputs.get("变量名")` 而非 `args.get()`

### HTTP Request节点
- 直接调用外部API
- API Key配置为环境变量

### 搜索工具节点
- 内置搜索引擎（Google/Bing/自定义）
- 适合无明确API的场景

## 参考文件

- `references/dify-workflow-architecture.md` — 详细架构、提示词模板、回溯算法
