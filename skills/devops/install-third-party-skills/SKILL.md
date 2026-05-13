---
name: install-third-party-skills
description: 从 GitHub 安装第三方 Hermes Agent skills 的标准流程。clone → 定位 SKILL.md → 拷贝到 skills 目录 → 清理临时文件。适用于 agent-browser、marketing-skills、context7 等外部 skill 仓库。
version: 1.0.0
tags: [skills, install, github, setup]
---

# 安装第三方 Skills

## 触发条件
- 用户要求安装某个 GitHub 上的 skill
- 对比现有 skills 后决定新增
- 从 awesome-hermes-agent 或 skills hub 发现新 skill

## 标准流程

1. **Clone 仓库到 /tmp**
   ```bash
   cd /tmp && git clone https://github.com/<owner>/<repo>.git
   ```

2. **定位 SKILL.md 文件**
   ```bash
   find /tmp/<repo> -name 'SKILL.md' | sort
   ```
   常见目录结构：
   - `<repo>/skills/<skill-name>/SKILL.md` — 最常见
   - `<repo>/skill-data/core/SKILL.md` — 部分仓库有完整参考文档

3. **确定目标分类目录**
   - `web/` — 浏览器/爬虫相关
   - `tools/` — CLI工具/包管理器
   - `marketing/` — 营销/CRO/SEO
   - `software-development/` — 开发工具
   - `productivity/` — 文档/效率工具
   - `research/` — 研究相关
   - 不确定时放 `tools/`

4. **拷贝 skill 内容**
   - 单个 skill：`cp -r /tmp/<repo>/skills/<name> ~/.hermes/skills/<category>/<name>/`
   - 多个 skill（整个 skills 目录）：`cp -r /tmp/<repo>/skills/* ~/.hermes/skills/<category>/`
   - 有 references/templates 子目录的也要一起拷贝

5. **验证安装**
   ```bash
   ls ~/.hermes/skills/<category>/<name>/SKILL.md
   head -5 ~/.hermes/skills/<category>/<name>/SKILL.md
   ```

6. **清理临时文件**
   ```bash
   rm -rf /tmp/<repo>
   ```

7. **同步到 Claude Code**（必须！否则 CC 的 `skills list` 看不到）
 ```bash
 # Hermes 读 ~/.hermes/skills/，Claude Code 读 ~/.claude/skills/
 # 用 symlink 共享，零额外磁盘占用
 
 # 单个 skill：
 ln -sf ~/.hermes/skills/<category>/<name> ~/.claude/skills/<name>
 
 # 批量同步所有 skill（用分类前缀避免同名冲突）：
 find ~/.hermes/skills -name 'SKILL.md' | while read f; do
     dir=$(dirname "$f")
     rel=${dir#*skills/}
     name=$(echo "$rel" | tr '/' '-')
     ln -sf "$dir" ~/.claude/skills/"$name"
 done
 ```
 **命名规则**：link名用 `分类-技能名`（如 `creative-web-design-engineer`），避免不同分类下同名目录冲突。
 **空间占用**：symlink 只占指针大小（~1KB/个），实际数据不复制，零额外磁盘。

8. **生效**：Hermes 下次 gateway 重启自动加载；Claude Code 下次启动自动加载。

## 已安装的第三方 Skills

| Skill | 来源 | Hermes路径 | CC link名 |
|-------|------|-----------|-----------|
| agent-browser | vercel-labs/agent-browser | web/agent-browser/ | web-agent-browser |
| context7-skills | narumiruna/context7-skills-skill | tools/context7-skills/ | tools-context7-skills |
| marketing (40个) | coreyhaines31/marketingskills | marketing/ | marketing-* |
| web-design-engineer | ConardLi/garden-skills | creative/web-design-engineer/ | creative-web-design-engineer |
| gpt-image-2 | ConardLi/garden-skills | creative/gpt-image-2/ | creative-gpt-image-2 |
| rag-skill | ConardLi/garden-skills | tools/rag-skill/ | tools-rag-skill |

## Pitfalls
- **Hermes vs Claude Code 目录隔离**：两系统读不同目录（Hermes→`~/.hermes/skills/`，CC→`~/.claude/skills/`），安装skill时**两边都要处理**，否则CC的`skills list`看不到新skill。
- **skill-data 目录**：部分仓库（如 agent-browser）的完整 skill 内容在 `skill-data/` 而非 `skills/`。`skills/` 下只是发现用的 stub。务必检查两个目录。
- **分类冲突**：如果已有同名 skill（如内置 marketing skill），第三方版本会覆盖。建议放不同子目录。
- **依赖检查**：部分 skill 需要 CLI 工具（如 agent-browser 需要 npm 安装）。SKILL.md 会说明，但不自动安装。
- **execute_code 循环上限**：批量创建symlink时，execute_code有50次tool call上限，大量skill会被截断。改用terminal跑shell脚本一次性完成。
- **Claude Code skill数量上限**：CC的`skills list`在skill过多时（>100个）会超时卡死。建议只同步CC实际会用到的skill（30-40个），砍掉marketing/mlops/email/media/smart-home/social等CC不触发的类别。这些skill仍保留在Hermes侧完整可用。
- **批量同步用短名**：给CC的symlink用简短无前缀名（如`web-design-engineer`而非`creative-web-design-engineer`），只有同名冲突时才加前缀。CC加载更快。
- **绝不在Hermes侧删skill**：减少CC共享的skill ≠ 删Hermes侧的冷备skill。磁盘冷备不占context，只有skill_view加载时才消耗token。用户说"取消一部分"默认指CC侧减负，除非明确说"从Hermes也删掉"。
