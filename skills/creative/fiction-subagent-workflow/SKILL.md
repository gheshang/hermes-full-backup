---
name: fiction-subagent-workflow
description: 小说创作+审查的双子agent工作流。写作委托Claude Code，审查用hermes-agent。含skill同步、超时兜底、审查报告驱动重写的完整流程。
triggers:
  - 用户要求委托子agent写小说/创作内容
  - 需要并行写作+审查的创作任务
---

# 小说创作双子Agent工作流

## 流程

### Variant A：从零创作 → 审查

标准流程，适用于用户要求写新小说。

### Variant B：修改已有小说（带括号内联标注） → 审查

用户已有小说草稿，文中段落/句子后有括号标注修改方向（如"（比喻不当，河里的石头会滚动）""（表达有问题）"）。

**输入预处理：**
- 源文件可能是 `.doc`（WPS Office 生成）而非 `.docx` → pandoc 和 python-docx 无法读取
- `.doc` 是 OLE2 容器格式，用 `olefile` 库解析 WordDocument 流，`struct.unpack('<H')` 逐双字节提取 UTF-16LE 文本
- 正文末尾有 OLE 垃圾字符（参考 `references/wps-doc-extraction.md`），提取后必须截断清理
- 飞书接收的 .doc 可能为空文件（0 bytes），实际内容在 `/home/hangskf/.hermes/cache/documents/doc_*.doc` 路径下

**修改步骤：**
1. 通读全文，提取所有括号标注（每处标注=一个修改点）
2. 将修改点按优先级分级：P0（结构/结尾大改）> P1（逻辑问题）> P2（表达/深度）> P3（细节/情节），逐级处理
3. 括号标注是"批评/问题描述"，非直接修改指令。执行者需理解问题本质，自行设计修改方案
4. 修改后删除所有括号标注及内容，保留纯净正文
5. 加载 `knowledge-comic-novel`（叙事学框架），加载 `humanizer`（去AI腔、自然口语化，**主 skill**）
6. 可选：加载 `chinese-touch-ups`（需安装 `hermes skills install lobehub/chinese-touch-ups`）
   - **冲突规则**：`humanizer`（自然口语化）与 `chinese-touch-ups`（典雅修辞）方向相反时，`humanizer` 优先
7. 逐处 patch 修改；`patch` 匹配失败时 fallback 到 `write_file` 重写整段
8. 全文改完后做一致性检查：确认 P0 修改不冲突 P1/P2 上下文（如改第十二章结尾不影响第三章角色定位）
9. `hemingway-iceberg-fiction`（冰山写法）不默认启用——用户需明确要求时才加载

**审核步骤：**
- 用 `delegate_task` 启动子 agent，加载 `knowledge-comic-novel` skill
- 审核维度：叙事学 8 维度 + 逻辑严谨度 + 行文通顺度 + 比喻恰当度 + 意味深长度 + 深度与通俗平衡 + 人物立体度 + 对话自然度 + 结尾力量 + 评分（15 维）
- timeout 设 600s（10 分钟），超时则当前 session 直接读审核报告
- 审核结果含分项评分表和改进优先级建议（★★★★★ → 立即修，★★☆☆☆ → 可忽略）

**审核后修改：**
- 按审核报告的优先级逐项实施（如符号回收 > 对话碎片化 > 配角深度 > 比喻精简 > 标点修正）
- 修改后需再次通读，确保 patch 未引入标点断裂或段落重复

**输出：**
- 修改版全文（`v5.md` 或更高版本号）
- 改动清单
- 审核报告（含 ASCII 张力曲线图、逐角色弧线分析、分项评分表）

### 1. Skill同步
- Hermes侧skill在 `~/.hermes/skills/`
- Claude Code侧在 `~/.claude/skills/`
- 同步方式：`ln -s ~/.hermes/skills/<skill-dir> ~/.claude/skills/<skill-dir>`
- 知识漫画小说必须同步：`knowledge-comic-novel`（含叙事学家角色）

### 2. 并行启动
- 写作子agent：Claude Code（`claude-code` skill）
  - 传入：前版全文 + 写作要求 + 相关skill内容
  - 超时风险：长文本创作容易超时
- 审查子agent：hermes-agent（`hermes-agent` skill）
  - 传入：待审文本 + 叙事学家角色（从knowledge-comic-novel skill加载）
  - 稳定性优于Claude Code

### 3. 超时兜底
- 如果写作子agent超时但审查已完成 → 基于审查报告自己写，比再委托一轮更快
- 审查报告本身就是精确的修改指令，直接执行即可

### 4. 版本管理
- 每版保存为独立文件：`v1.md`, `v2.md`, ...
- 记录每版字数和核心改动
- 投递格式：改动清单 + 全文

## 经验
- hermes-agent做审查比Claude Code稳定（不会超时）
- Claude Code做长文本创作容易超时，考虑拆分章节或增加timeout
- 审查报告的价值 = 精确诊断 + 优先级排序，可以直接当修改蓝图
- **`delegate_task` 可同时用于修改和审核**：在无 Claude Code 安装或用户明确要求单模型时，`delegate_task` 用当前模型（如 deepseek-v4-pro）启动子 agent 即可完成两阶段工作。审核子 agent 设置 `toolsets=["terminal","file","search","skills"]`、timeout=600s；修改子 agent 设置 `toolsets=["terminal","file"]`。实测 deepseek-v4-pro 在 10 分钟内可完成 15 维叙事学审核 + 分项评分表输出。
