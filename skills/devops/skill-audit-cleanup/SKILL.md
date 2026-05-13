---
name: skill-audit-cleanup
description: |
  审查并清理 Hermes Agent skill 目录——识别重复、环境不兼容、废弃的 skill，
  以及更新 memory 中的路由表。当用户要求"审查skill""清理skill""skill太多"时触发。
---

# Skill 审查与清理流程

## 触发条件
- 用户主动要求审查/清理 skill
- 安装新 skill 包后怀疑有重复
- skill 列表过长导致系统 prompt 臃肿

## 审查步骤

### 1. 盘点全量
```bash
find ~/.agents/skills ~/.hermes/skills -name 'SKILL.md' | sed 's|/SKILL.md||;s|.*/||' | sort -u
```

### 2. 识别重复（同名两版本）
常见模式：`bare-name` ↔ `superpowers-bare-name`
- 对比两份 SKILL.md 的 diff 行数：`diff file1 file2 | wc -l`
- 如果 diff > 0 但功能描述相同 → 保留系统可见列表中的那个版本，删另一个
- 判断哪个被系统加载：看 available_skills 列表里的名称

### 3. 识别环境不兼容
- Apple 系 skill（apple-notes, apple-reminders, findmy, imessage）在 Linux VPS 上无用
- 依赖特定硬件/OS 的 skill → 直接删

### 4. 识别废弃 skill
- 对应项目已删除的 skill（如 tencentyun-seckill 项目已删但 skill 还在）
- 长期未使用的游戏类 skill（pokemon-player, minecraft-modpack-server）→ 确认后删

### 5. 识别功能重叠（不删，标记互补）
- 同领域多个 skill 如果覆盖不同场景（如 html-ppt 技术风 vs guizang-ppt 杂志风 vs powerpoint .pptx格式），属于互补不是重复
- 仅在功能完全覆盖（子集关系）时才删其中一个

## 清理执行

```bash
# 删除目标 skill 目录（根据审查结果替换名称）
rm -rf ~/.hermes/skills/<category>/<skill-name>
rm -rf ~/.agents/skills/<skill-name>
```

## 更新 Memory 路由表

审查后同步更新 `~/.hermes/memories/MEMORY.md` 中的 skill 路由段：
- 只列出需要主动路由的 skill（系统不会自动匹配的那些）
- 不写"其余靠触发词"这种废话
- 格式：场景 → skill名，一行一条，不用嵌套列表

## 历史清理记录

### 2026-04-30 第二次审查
- 重命名8个目录使其与SKILL.md内部name字段一致（消除维护混淆）：
  audiocraft→audiocraft-audio-generation, lm-evaluation-harness→evaluating-llms-harness,
  segment-anything→segment-anything-model, trl-fine-tuning→fine-tuning-with-trl,
  vllm→serving-llms-vllm, creative-ideation→ideation, rag-skill→kb-retriever,
  maoxuan-skill→mao-zedong-perspective
- 删daily-self-audit中重复的v3.1架构表（与v4段内容重复）
- 审查10组疑似功能重叠skill，全部为互补关系，无需删除：
  marketing/image vs creative/*, marketing/video vs video-prompting,
  social-content vs xurl, seo-audit vs ai-seo, copywriting vs copy-editing,
  email-sequence vs cold-email, competitor-profiling vs competitor-alternatives,
  disk-space-audit vs daily-self-audit, agent-browser vs core,
  research-paper-writing vs arxiv
