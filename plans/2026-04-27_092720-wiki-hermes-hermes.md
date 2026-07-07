# 计划：Hermes Agent 中文使用手册

## 目标

基于本地wiki库 + 网上资源，产出一份**完备、通俗、有例子**的中文Hermes使用手册。分多篇交付避免上下文过长。

## 当前上下文

- 本地wiki：~/.hermes/wiki/，含官方文档全文（slash commands、CLI commands、tools、skills、memory、cron、MCP、profiles、hooks、sessions等）
- 外部资源：heyuan110.com深度评测、DataCamp教程、官方文档站
- 用户已在用Hermes（飞书+微信+CLI），对基础概念有体感，手册应避免过于浅显但要保证自洽

## 手册结构（6篇）

| 篇 | 标题 | 核心内容 | 预估字数 |
|---|------|---------|---------|
| P1 | 概览与快速上手 | Hermes是什么、核心架构（五层Harness）、安装、首次配置、chat基本交互 | 3000 |
| P2 | 斜杠命令全表 | CLI斜杠命令 + 消息平台斜杠命令，分类表+用法示例 | 3000 |
| P3 | 工具与技能系统 | 40+工具分类速查、toolset配置、skill创建/安装/调用、skill vs memory区别 | 3000 |
| P4 | 记忆、会话与多Profile | memory三层体系、session管理/搜索/resume、profile创建与多Agent并行 | 3000 |
| P5 | 定时任务、钩子与MCP | cron创建/管理/deliver、shell hooks/gateway hooks/plugin hooks、MCP server配置与工具过滤 | 3000 |
| P6 | 消息平台与进阶技巧 | 飞书/微信/Telegram/Discord配置、gateway管理、语音模式、fallback/压缩/批量处理、实用tricks | 3000 |

## 写作原则

1. **通俗但不浅显**——假设读者会用终端和Python，不解释什么是API，但要解释Hermes特有的概念（如harness五层、skill渐进加载）
2. **有例子**——每个命令/配置至少一个实际可跑的示例
3. **中文原生**——不是翻译文档，而是按中文思维组织，术语附英文原文
4. **完备**——覆盖所有slash commands、所有顶层CLI命令、核心工具、核心配置项

## 交付方式

- 每篇独立markdown文件，保存到 `~/hermes-manual/`
- 文件命名：`P1-概览与快速上手.md` ~ `P6-消息平台与进阶技巧.md`
- 每篇写完后直接发飞书给用户审阅
- 全部完成后合并一份完整版

## 信息源

| 来源 | 覆盖内容 |
|------|---------|
| wiki: reference-slash-commands.md | 全部斜杠命令 |
| wiki: reference-cli-commands.md | 全部CLI命令 |
| wiki: features-tools.md | 工具与toolset |
| wiki: guides-work-with-skills.md | Skill系统 |
| wiki: guides-tips.md | 最佳实践 |
| wiki: memory.md | 记忆系统 |
| wiki: sessions.md | 会话管理 |
| wiki: profiles.md | 多Profile |
| wiki: cron-toolsets.md | Cron |
| wiki: features-hooks.md | Hooks |
| wiki: hermes-mcp-config.md | MCP配置 |
| wiki: hermes-environment-variables.md | 环境变量 |
| wiki: features-fallback-providers.md | Fallback |
| wiki: features-voice-mode.md | 语音模式 |
| wiki: features-batch-processing.md | 批量处理 |
| web: heyuan110.com | Harness五层架构、对比视角 |
| web: DataCamp tutorial | 教程结构参考 |
| 实际使用经验 | cron/deliver/skill/memory实操 |

## 执行步骤

1. 写P1（概览与快速上手）
2. 写P2（斜杠命令全表）
3. 写P3（工具与技能系统）
4. 写P4（记忆、会话与多Profile）
5. 写P5（定时任务、钩子与MCP）
6. 写P6（消息平台与进阶技巧）
7. 合并完整版

## 验证

- 每篇命令示例可执行性检查（至少语法正确）
- 覆盖率检查：slash commands全表 vs 手册内容逐项核对
- 用户审阅反馈迭代

## 风险

- wiki部分源文档是Claude Code文档混入（如memory.md、cli-usage.md），需注意区分Hermes特有 vs Claude Code特有
- 手册过长可能超出单次上下文，必须分篇执行
