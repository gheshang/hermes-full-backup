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
- **文档生成（Markdown→docx，基于模板+知识库+LLM 混合填充）**
- 联网检索+数据整合（搜索+LLM提取）
- 工业/电力/医疗等专业领域自动化

## 核心设计原则

### 文档生成场景：Markdown → pandoc → docx

**AI 自由生成内容 vs 占位符模板的取舍：**
- 章节数量不固定、表格行列不固定、条件性内容 → 用 **Markdown** 让 AI 自由生成
- 格式控制（字体、行距、页眉页脚）→ 用 **pandoc + reference-docx** 预先调好的样式模板
- 各管各的，AI 管内容，模板管格式

**不推荐 docxtpl（python-docx-template）用于文档报告场景**——占位符模式不够灵活，且不支持页眉页脚、交叉引用、自动目录等 Word 特性。

详见 `references/construction-plan-generation.md`。

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
- `references/enterprise-alert-system.md` — 企业告警系统工作流设计模式
- `references/construction-plan-generation.md` — 施工方案报告自动生成设计模式（Markdown→docx、10章节标准模板、知识库策略）
- `references/knowledge-qa-question-router.md` — 知识库问答+问题分类路由工作流（法规规章场景，含分类器/条件分支/多策略检索/报告生成）
