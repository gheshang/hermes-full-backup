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

## 选择策略与风险管理

### 核心原则：按需挑选，不要全量安装

大型第三方技能库（如 mattpocock/skills 约40+个）全量安装会导致：

1. **上下文膨胀** — Agent 每次收到指令需遍历所有 SKILL.md 匹配，token 消耗剧增
2. **技能冲突** — 功能相近的技能（如 `to-prd`、`write-a-prd`、`prd-to-plan`）触发条件不同，Agent 容易困惑
3. **环境依赖失效** — 部分技能需要特定环境（Git仓库、练习目录等），在无关场景下毫无用处

### 推荐安装流程

**第一步：只装核心3个**
```
diagnose          # 遇到bug/错误时必用，解决80%的问题
tdd               # 写代码时强制测试先行，防止返工
review            # 提交前自动审查，减少低级错误
```

**第二步：按项目阶段动态添加**
- 需求阶段 → `write-a-prd` + `to-issues`
- 架构阶段 → `zoom-out` + `improve-codebase-architecture`
- 原型阶段 → `prototype`
- 交接场景 → `handoff`

**第三步：定期审计**
- 每月检查 `ls ~/.hermes/skills/<category>/`，超过3个月未调用的技能直接删除
- 不要指望 Agent 自动推荐技能 — 只会更混乱。你决定何时调用哪个技能

### 安装前自检问题
```
我最近一周有没有用过类似功能？
这个技能解决的具体问题是什么？
如果不用这个技能，我能用什么替代？
```
任一答案为"否" → 暂缓安装

## 更新已有 Skill（非首次安装）

当用户要求从 GitHub 同步更新已安装的 skill 时，**不要直接删除整个目录**。SKILL.md 可能包含 Hermes YAML frontmatter（name/description/tags），repo 版本可能没有——删了再拷贝会丢失 frontmatter。

采用**文件级同步**策略：

### 步骤

1. **备份旧版**
   ```bash
   SKILL_DIR="~/.hermes/skills/<category>/<name>"
   BACKUP="/tmp/<name>-backup-$(date +%Y%m%d_%H%M%S)"
   cp -r "$SKILL_DIR" "$BACKUP"
   ```

2. **Clone 最新仓库**
   ```bash
   cd /tmp && git clone --depth 1 https://github.com/<owner>/<repo>.git
   ```
   （`--depth 1` 只拉最新 commit，节省时间和磁盘）

3. **比对目录结构，识别新增/删除文件**
   ```bash
   # 查看 repo 文件列表
   cd /tmp/<repo>/path/to/skill
   find . -not -path './.git/*' -not -name '.git' -type f | sort
   
   # 查看已安装文件列表
   find ~/.hermes/skills/<category>/<name> -type f | sort
   ```
   标记出：repo 有但本地没有的（新增）、本地有但 repo 没有的（已废弃）、两者都有的（需同步）

4. **处理 SKILL.md（关键步骤）**
   ```bash
   # 检查 repo 的 SKILL.md 是否包含 Hermes frontmatter（以 "---\nname:" 开头）
   head -5 /tmp/<repo>/path/to/skill/SKILL.md
   
   # 情况 A：repo 有 frontmatter → 直接覆盖
   cp /tmp/<repo>/path/to/skill/SKILL.md "$SKILL_DIR/SKILL.md"
   
   # 情况 B：repo 没有 frontmatter → 提取 body，拼接 Hermes frontmatter
   # 保留当前 frontmatter，只替换 body 部分
   old_frontmatter=$(head -5 "$SKILL_DIR/SKILL.md")
   tail -n +2 /tmp/<repo>/path/to/skill/SKILL.md > /tmp/new-body.md
   cat <(echo "$old_frontmatter") /tmp/new-body.md > "$SKILL_DIR/SKILL.md"
   ```

5. **同步子目录（逐类覆盖）**
   ```bash
   # assets/（模板文件、图片、js）
   cp /tmp/<repo>/path/to/skill/assets/* "$SKILL_DIR/assets/"
   
   # references/（文档）
   cp /tmp/<repo>/path/to/skill/references/* "$SKILL_DIR/references/"
   
   # scripts/（校验脚本等）
   cp /tmp/<repo>/path/to/skill/scripts/* "$SKILL_DIR/scripts/"
   ```

6. **处理已废弃的文件**
   ```bash
   # repo 没有但本地残留的文件，确认后清理
   # 例如：references/report-to-ppt-extraction.md 被 repo 移除
   rm -f "$SKILL_DIR/references/old-reference.md"
   ```

7. **验证：完整 diff 确认一致性**
   ```bash
   # SKILL.md 应该完全一致（如果 repo 有 frontmatter）
   diff /tmp/<repo>/path/to/skill/SKILL.md "$SKILL_DIR/SKILL.md"
   
   # 文件数量一致（允许 repo 删除了文件）
   echo "Repo files:" && find /tmp/<repo>/path/to/skill -type f | wc -l
   echo "Installed files:" && find "$SKILL_DIR" -type f | wc -l
   ```

8. **清理临时文件**
   ```bash
   rm -rf /tmp/<repo>
   ```

9. **（可选）检查并更新 Claude Code symlink**
   如果更新了 SKILL.md，CC 侧不会自动感知——但 CC 在下次 `/skill` 加载时会重新读取文件内容，所以 symlink 不需要重建。如果 skill 被重命名或移动到新分类，才需要重建 symlink。

## Pitfalls
- **技能过载（Skill Overload）** — 大型技能库全量安装会导致上下文膨胀、技能冲突、环境依赖失效。务必按需挑选，核心3个起步，动态添加。参考 `references/skill-selection-guide.md`。
- **更新 Skill 前必须备份**：直接 `rm -rf` 后拷贝新版。不备份的话，如果新版有问题无法回滚。备份到 `/tmp/<name>-backup`，确认新版验证通过后再清理。
- **旧 symlink 指向废弃路径**：CC 的 `~/.claude/skills/` 下可能残留指向 `/home/hangskf/.agents/skills/` 的旧 link。更新/安装前先 `ls -la ~/.claude/skills/<name>` 检查，如果指向错误路径，先 `rm` 再重新 `ln -sf`。
- **Hermes vs Claude Code 目录隔离**：两系统读不同目录（Hermes→`~/.hermes/skills/`，CC→`~/.claude/skills/`），安装skill时**两边都要处理**，否则CC的`skills list`看不到新skill。
- **skill-data 目录**：部分仓库（如 agent-browser）的完整 skill 内容在 `skill-data/` 而非 `skills/`。`skills/` 下只是发现用的 stub。务必检查两个目录。
- **分类冲突**：如果已有同名 skill（如内置 marketing skill），第三方版本会覆盖。建议放不同子目录。
- **依赖检查**：部分 skill 需要 CLI 工具（如 agent-browser 需要 npm 安装）。SKILL.md 会说明，但不自动安装。
- **execute_code 循环上限**：批量创建symlink时，execute_code有50次tool call上限，大量skill会被截断。改用terminal跑shell脚本一次性完成。
- **Claude Code skill数量上限**：CC的`skills list`在skill过多时（>100个）会超时卡死。建议只同步CC实际会用到的skill（30-40个），砍掉marketing/mlops/email/media/smart-home/social等CC不触发的类别。这些skill仍保留在Hermes侧完整可用。
- **批量同步用短名**：给CC的symlink用简短无前缀名（如`web-design-engineer`而非`creative-web-design-engineer`），只有同名冲突时才加前缀。CC加载更快。
- **绝不在Hermes侧删skill**：减少CC共享的skill ≠ 删Hermes侧的冷备skill。磁盘冷备不占context，只有skill_view加载时才消耗token。用户说"取消一部分"默认指CC侧减负，除非明确说"从Hermes也删掉"。
