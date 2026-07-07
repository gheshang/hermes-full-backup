---
name: opencode-manual
description: OpenCode CLI 完整操作手册 — 通俗易懂版
version: 2.0.0
author: 上河一号
license: MIT
metadata:
  hermes:
    tags: [opencode, manual, 操作手册, 中文, wiki, 通俗易懂]
    related_skills: [opencode, claude-code, codex, hermes-agent, llm-wiki]
---

# OpenCode CLI 中文操作手册（通俗版）

> 基于 `~/wiki/opencode/` 知识库（77 个文档）与 `autonomous-ai-agents/opencode/SKILL.md` 整合编写
> 目标：让任何水平的开发者都能看懂、会用
> 最后更新：2026-05-19

---

## 写作风格指南

**核心原则：通俗易懂，拒绝技术黑话。**

- 用"是啥""怎么配""能干嘛"代替"概述""配置项""功能说明"
- 用表格代替大段文字描述
- 每个概念先给一句话人话解释，再展开细节
- 命令示例配一行注释说明干啥
- 陷阱和注意事项用 ⚠️ 标记，放在显眼位置
- 避免"综上所述""值得注意的是"等 AI 腔
- 技术术语第一次出现时必须解释

**用户偏好**：当用户说"通俗易懂"或"不要那么技术"时，立即切换到这种风格。
> 最后更新：2026-05-19

---

## 写作风格规范（重要）

本手册的写作风格是用户明确要求的"**通俗易懂**"，后续更新必须遵守：

1. **用口语化中文**：用"是啥""怎么配""能干嘛"代替"概述""配置方法""功能说明"
2. **先给结论再给细节**：每节开头用一句话总结核心内容
3. **多用表格和场景对照**：避免大段纯文字，用表格对比选项、用场景说明用途
4. **代码示例配注释**：每段代码都要有 `# 注释` 说明在干嘛
5. **避免术语堆砌**：遇到专业术语（如 MCP、LSP、ACP）先用一句话解释
6. **给推荐值**：配置项不要只列选项，要给出推荐值和理由
7. **给避坑提示**：每个功能点都要标注 ⚠️ 注意事项或 💡 技巧
8. **章节标题用问句**：§1 这是什么？§2 怎么装？§6 模型怎么选？——让用户一眼知道这节讲啥

**不要做**：
- 不要写成技术文档风格（"本章节介绍..."、"该配置项用于..."）
- 不要大段复制 wiki 原文而不消化
- 不要罗列命令而不解释使用场景
- 不要假设用户已经懂上下文

### 内容完整性检查清单

每次更新手册前，对照 wiki 知识库检查是否覆盖：

| 检查项 | 状态 |
|--------|------|
| 所有 21 个 Entities 文件都有对应章节 | ✅ |
| 所有 19 个 Concepts 文件都有对应章节 | ✅ |
| 权限控制（细粒度模式匹配）已覆盖 | ✅ |
| 自定义命令（参数/Shell 注入/文件引用）已覆盖 | ✅ |
| IDE 集成（VS Code/Zed/JetBrains/Neovim）已覆盖 | ✅ |
| 企业部署（SSO/内部网关/私有 NPM）已覆盖 | ✅ |
| 插件系统（加载方式/事件类型/开发示例）已覆盖 | ✅ |
| SDK（Python + TypeScript）已覆盖 | ✅ |
| 常见问题（PATH/TUI 卡住/模型错误/权限/上下文）已覆盖 | ✅ |
| wiki 索引（Entities + Concepts + Raw）已完整列出 | ✅ |

---

## 目录

1. [这是什么？](#1-这是什么)
2. [怎么装？](#2-怎么装)
3. [怎么配？](#3-怎么配)
4. [命令速查](#4-命令速查)
5. [TUI 怎么用](#5-tui-怎么用)
6. [模型怎么选](#6-模型怎么选)
7. [代理是什么](#7-代理是什么)
8. [工具与权限](#8-工具与权限)
9. [MCP 扩展](#9-mcp-扩展)
10. [GitHub 自动化](#10-github-自动化)
11. [IDE 里怎么用](#11-ide-里怎么用)
12. [Web 界面](#12-web-界面)
13. [Hermes 里怎么用 OpenCode](#13-hermes-里怎么用-opencode)
14. [自定义命令和工具](#14-自定义命令和工具)
15. [Agent Skills](#15-agent-skills)
16. [常见问题](#16-常见问题)
17. [OpenCode vs Claude Code](#17-opencode-vs-claude-code)
18. [企业怎么用](#18-企业怎么用)
19. [插件和生态](#19-插件和生态)
20. [SDK 开发](#20-sdk-开发)
21. [附录：wiki 知识库索引](#21-附录-wiki-知识库索引)

---

## 1. 这是什么？

### 1.1 一句话介绍

**OpenCode 是一个开源的 AI 编程助手**，装在终端里，能帮你写代码、改代码、查 bug、写测试、做代码审查——就像有个程序员同事一直在你旁边帮你干活。

### 1.2 它有多厉害？

| 数据 | 说明 |
|------|------|
| GitHub 160K+ stars | 比很多大厂开源项目都火 |
| 650 万+ 月活开发者 | 真有人在用，不是纸上谈兵 |
| 75+ 个 AI 模型可选 | Claude、GPT、Gemini、本地模型随便挑 |
| 完全开源 | 代码随便看，想改就改 |

### 1.3 它能帮你做什么？

| 你想做的事 | OpenCode 能怎么帮 |
|-----------|-----------------|
| "帮我写个登录功能" | 直接生成代码，能改能跑 |
| "这段代码为啥报错？" | 读代码 + 看报错，告诉你原因和修复方案 |
| "帮我改一下这个函数" | 精准修改，不碰其他代码 |
| "帮我写单元测试" | 按你的代码风格写测试 |
| "帮我 review 这个 PR" | 找出 bug、安全风险、风格问题 |
| "帮我查一下这个库怎么用" | 自动搜文档、看源码 |
| "帮我重构这个模块" | 制定计划 → 执行 → 验证 |

### 1.4 它和 Claude Code 有啥区别？

一句话：**OpenCode 更自由，Claude Code 更省心。**

| 方面 | OpenCode | Claude Code |
|------|---------|-------------|
| 开源吗 | ✅ 完全开源 | ❌ 闭源 |
| 能用哪些模型 | 75+ 个，随便换 | 只能用 Claude |
| 能用本地模型吗 | ✅ 可以（Ollama 等） | ❌ 不行 |
| 贵吗 | API 按量付费，有免费模型 | Claude Pro 每月 20 刀 |
| 上手难度 | 稍高（配置多一点） | 开箱即用 |

**选 OpenCode**：想要模型自由、预算有限、想本地跑模型、想完全掌控工具。
**选 Claude Code**：只想快点开始干活、相信 Claude 模型最强、已经有 Claude Pro。

---

## 2. 怎么装？

### 2.1 最快的安装方式（推荐）

一行命令搞定：

```bash
curl -fsSL https://opencode.ai/install | bash
```

装完就能用。

### 2.2 其他方式

**如果你用 Homebrew（macOS / Linux）：**
```bash
brew install anomalyco/tap/opencode
```

**如果你用 npm：**
```bash
npm install -g opencode-ai
```

**如果你用 Docker：**
```bash
docker run -it --rm ghcr.io/anomalyco/opencode
```

### 2.3 怎么验证装好了？

```bash
opencode --version    # 看版本号
which opencode        # 看安装位置
opencode auth list    # 看有没有配置 API Key
```

### 2.4 第一步：配置 API Key

OpenCode 本身免费，但调用 AI 模型需要 API Key。有三种方式：

**方式一：TUI 里交互式配置（最简单）**
```bash
opencode
/connect   # 选 opencode → 打开网页登录 → 复制 Key → 粘贴
```

**方式二：命令行**
```bash
opencode auth login
```

**方式三：环境变量（适合服务器）**
```bash
export OPENROUTER_API_KEY="sk-or-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

> 💡 **省钱技巧**：用 OpenRouter 可以免费用到一些模型（如 Qwen、Llama），先试试零成本。

### 2.5 初始化你的项目

```bash
cd /你的/项目/目录
opencode
/init   # 自动生成 AGENTS.md 文件
```

这个 `AGENTS.md` 文件很重要——它告诉 OpenCode 你的项目结构、编码规范、常用命令等。建议提交到 Git，这样团队成员都能受益。

---

## 3. 怎么配？

### 3.1 配置文件长啥样？

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "autoupdate": true,
  "permission": {
    "edit": "ask",
    "bash": "allow"
  }
}
```

### 3.2 配置文件有哪些？优先级咋样？

OpenCode 会从多个地方读配置，**后面的覆盖前面的**：

| 优先级（低→高） | 配置文件 | 用来干嘛 |
|----------------|---------|---------|
| 1 | `.well-known/opencode` | 公司统一配置（远程） |
| 2 | `~/.config/opencode/opencode.json` | 你个人的偏好 |
| 3 | `OPENCODE_CONFIG` 环境变量 | 临时指定配置文件 |
| 4 | 项目根目录 `opencode.json` | 这个项目特有的配置 |
| 5 | `.opencode/` 目录 | 代理、命令、插件等 |
| 6 | `OPENCODE_CONFIG_CONTENT` | 直接写 JSON 内容 |

> 简单说：**项目配置 > 个人配置 > 公司配置**。

### 3.3 常用配置项

| 配置项 | 是啥 | 推荐值 |
|--------|-----|--------|
| `model` | 默认用哪个模型 | `anthropic/claude-sonnet-4-5` |
| `small_model` | 简单任务用轻量模型 | `openai/gpt-4o-mini`（省钱） |
| `autoupdate` | 自动更新吗 | `true` |
| `snapshot` | 记录代码变更吗 | `true`（推荐，方便撤销） |
| `share` | 会话分享模式 | `"manual"`（默认，安全） |

### 3.4 用环境变量里的值

```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "openai": {
      "options": { "apiKey": "{env:OPENAI_API_KEY}" }
    }
  }
}
```

这样可以在不同环境（开发/生产）用不同的 Key，不用改配置文件。

---

## 4. 命令速查

### 4.1 最常用的几个命令

| 命令 | 干啥 |
|------|-----|
| `opencode` | 启动交互式界面（TUI） |
| `opencode /path/to/project` | 启动并指定项目目录 |
| `opencode -c` | 继续上次的会话 |
| `opencode -s ses_xxx` | 继续指定 ID 的会话 |
| `opencode run "..."` | 一次性执行命令后退出 |
| `opencode --version` | 看版本号 |

### 4.2 `opencode run` 的常用参数

```bash
# 一次性任务：修复 lint 错误
opencode run "Fix all lint errors in the project"

# 附加文件
opencode run "Review this config" -f config.yaml -f .env.example

# 指定模型
opencode run "Refactor auth module" --model openrouter/anthropic/claude-sonnet-4

# 显示思考过程
opencode run "Debug why tests fail" --thinking

# 指定推理力度
opencode run "Complex refactoring" --variant high
```

### 4.3 子命令

| 子命令 | 干啥 |
|--------|-----|
| `opencode auth login/list/logout` | 管理 API Key |
| `opencode models` | 看有哪些模型可用 |
| `opencode models --verbose` | 看模型详情和价格 |
| `opencode session list` | 看历史会话 |
| `opencode stats` | 看用了多少 token、花了多少钱 |
| `opencode stats --days 7` | 看最近 7 天的用量 |
| `opencode mcp add/list` | 管理 MCP 服务器 |
| `opencode github install` | 一键配置 GitHub 集成 |

---

## 5. TUI 怎么用

TUI 就是那个终端里的交互界面，长得像聊天窗口。

### 5.1 启动

```bash
opencode              # 当前目录
opencode /my/project  # 指定目录
```

### 5.2 三种模式（用 Tab 切换）

| 模式 | 按 Tab 到 | 能干啥 |
|------|----------|-------|
| **Ask** | 默认 | 只问不改，像聊天 |
| **Plan** | 第 1 次 Tab | 制定计划，但不改代码 |
| **Build** | 第 2 次 Tab | 真正改代码 |

**推荐流程**：先 Ask 问清楚 → 再 Plan 看方案 → 最后 Build 执行。

### 5.3 斜杠命令（`/` 开头）

| 命令 | 干啥 |
|------|-----|
| `/init` | 生成/更新 AGENTS.md |
| `/connect` | 添加 API Key |
| `/new` | 新建一个会话 |
| `/sessions` | 看/切换会话 |
| `/models` | 看可用模型 |
| `/compact` | 压缩上下文（省 token） |
| `/undo` | 撤销上次的修改 |
| `/redo` | 重做 |
| `/export` | 导出为 Markdown 文件 |
| `/share` | 生成分享链接 |
| `/exit` | 退出 |

### 5.4 怎么引用文件？

直接打 `@` 加文件名：

```
帮我看看 @src/api/auth.ts 里的登录逻辑有没有问题
```

OpenCode 会自动把文件内容读进来。

也可以用 `@文件#行号` 引用特定行：

```
解释一下 @src/utils/index.ts#25-40 这段代码
```

### 5.5 怎么运行 shell 命令？

用 `!` 开头：

```
!npm run build   # 运行构建
!git status      # 看 git 状态
```

命令的输出会直接插入到你的消息里。

### 5.6 快捷键

| 快捷键 | 干啥 |
|--------|-----|
| `Ctrl+X N` | 新建会话 |
| `Ctrl+X L` | 会话列表 |
| `Ctrl+X E` | 打开外部编辑器 |
| `Ctrl+X Q` | 退出 |
| `Ctrl+P` | 命令面板 |
| `Page Up/Down` | 滚动 |
| `Tab` | 切换模式（Ask → Plan → Build） |

### 5.7 会话分享

想和同事共享对话？用 `/share`：

```
/share
```

会生成一个链接（`opncd.ai/s/...`），发给同事就能看。

有三种分享模式：

| 模式 | 配置 | 说明 |
|------|-----|------|
| Manual（默认） | `"share": "manual"` | 手动点 `/share` 才分享 |
| Auto | `"share": "auto"` | 每个新对话自动分享 |
| Disabled | `"share": "disabled"` | 完全禁用分享 |

> ⚠️ **隐私提醒**：分享的对话包含完整聊天记录。敏感代码/密钥不要分享。分享完记得用 `/unshare` 取消。

---

## 6. 模型怎么选

### 6.1 有哪些模型能用？

75+ 个，包括：

| 提供商 | 代表模型 | 适合 |
|--------|---------|------|
| Anthropic | Claude Opus/Sonnet/Haiku | 复杂推理、代码生成 |
| OpenAI | GPT-4.1/GPT-4o | 综合任务 |
| Google | Gemini 2.0/2.5 | 多模态任务 |
| DeepSeek | DeepSeek V3/R1 | 中文场景、性价比 |
| 本地模型 | Qwen、Llama、Gemma | 隐私敏感、零成本 |

### 6.2 推荐模型

| 用途 | 推荐模型 |
|------|---------|
| 日常开发（性价比） | Claude Sonnet 4.5 |
| 复杂推理/架构设计 | Claude Opus 4.5 |
| 简单任务（省钱） | GPT-4o-mini / Haiku |
| 中文场景 | DeepSeek V3 / Qwen |
| 本地部署 | Qwen2.5-Coder-32B |

### 6.3 怎么设置默认模型？

在 `opencode.json` 里：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5"
}
```

### 6.4 本地模型怎么配？

```jsonc
{
  "provider": {
    "ollama": {
      "baseURL": "http://localhost:11434",
      "models": {
        "qwen2.5-coder:32b": {}
      }
    }
  }
}
```

先装 Ollama，拉模型：
```bash
ollama pull qwen2.5-coder:32b
```

---

## 7. 代理是什么

### 7.1 代理（Agent）就是不同"角色"的 AI

OpenCode 不是只有一个 AI，而是有多个**预设角色**，每个角色擅长不同的事。

### 7.2 内置代理

| 代理 | 角色 | 权限 | 怎么用 |
|------|-----|------|-------|
| **Build** | 干活的主力 | 所有工具都能用 | 默认就是这个 |
| **Plan** | 出主意的军师 | 不能改文件 | 按 Tab 切换过来 |
| **General** | 多面手 | 几乎全权限 | 自动调用 |
| **Explore** | 只读探索者 | 只能读，不能改 | 自动调用 |
| **Scout** | 外勤侦察兵 | 只读 + 搜外部文档 | 自动调用 |

### 7.3 怎么自定义代理？

**方式一：JSON 配置（`opencode.json`）**

```json
{
  "agent": {
    "code-reviewer": {
      "description": "专门做代码审查",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-5",
      "permission": { "edit": "deny", "bash": "ask" },
      "prompt": "{file:./prompts/review.txt}"
    }
  }
}
```

**方式二：Markdown 文件（`.opencode/agents/code-reviewer.md`）**

```markdown
---
description: 代码审查代理
mode: subagent
permission:
  edit: deny
  bash: deny
---
Focus on security vulnerabilities and performance issues.
```

### 7.4 自定义代理的配置项

| 选项 | 干啥 | 例子 |
|------|-----|------|
| `description` | 代理是干啥的（必填） | `"代码审查"` |
| `mode` | 主代理还是子代理 | `primary` / `subagent` |
| `model` | 用哪个模型 | `anthropic/claude-haiku` |
| `temperature` | 创造性（0=严谨，1=发散） | `0.3` |
| `max_steps` | 最多执行几步 | `10` |
| `prompt` | 自定义系统提示词 | `{file:./prompts/foo.txt}` |
| `hidden` | 是否在 `@` 补全里隐藏 | `true` |

---

## 8. 工具与权限

### 8.1 OpenCode 有哪些内置工具？

| 工具 | 干啥 |
|------|-----|
| `read` | 读文件 |
| `edit` | 精确替换文件内容 |
| `write` | 创建/覆盖文件 |
| `bash` | 执行 shell 命令 |
| `grep` | 正则搜索代码 |
| `glob` | 按模式找文件 |
| `lsp` | 语言服务器（看定义、跳转） |
| `skill` | 加载技能文件 |
| `webfetch` | 抓取网页 |
| `websearch` | 网络搜索 |

### 8.2 权限控制——不让 AI 乱改

你可以控制 AI 能不能自动执行某些操作：

```json
{
  "permission": {
    "*": "ask",       // 默认都问
    "bash": "allow",  // shell 命令自动执行
    "edit": "deny"    // 禁止改文件
  }
}
```

三个值：
- `"allow"` — 自动执行，不问
- `"ask"` — 每次都要你确认
- `"deny"` — 直接禁止

### 8.3 细粒度权限（高级）

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",       // git 命令自动放行
      "npm *": "allow",       // npm 命令自动放行
      "rm *": "deny"          // 禁止 rm
    },
    "edit": {
      "*": "deny",
      "src/components/*.tsx": "allow"  // 只允许改 components
    }
  }
}
```

### 8.4 LSP 语言服务器

OpenCode 会自动检测你的项目语言，启动对应的 LSP 服务器：

| 语言 | LSP 服务器 | 能干嘛 |
|------|-----------|-------|
| TypeScript/JavaScript | typescript-language-server | 类型检查、跳转定义 |
| Python | pyright | 类型检查 |
| Go | gopls | 代码补全、跳转 |
| Rust | rust-analyzer | 代码分析 |
| Java | jdtls | 代码分析 |
| CSS/Tailwind | tailwindcss-intellisense | Tailwind 提示 |

> 大部分语言开箱即用，不需要额外配置。

---

## 9. MCP 扩展

### 9.1 MCP 是啥？

MCP（Model Context Protocol）是一种**让 AI 连接外部工具的标准方式**。就像给 OpenCode 装插件，但它比传统插件更灵活。

### 9.2 能连哪些 MCP 服务器？

| MCP 服务器 | 能干嘛 |
|-----------|-------|
| Sentry | 看错误日志 |
| Context7 | 搜文档 |
| GitHub | 操作 GitHub（PR、Issue） |
| Brave Search | 网络搜索 |
| PostgreSQL | 查数据库 |

### 9.3 怎么配置？

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "enabled": true
    },
    "my-local-tool": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
      "enabled": true
    }
  }
}
```

### 9.4 CLI 管理

```bash
opencode mcp add <name>      # 添加
opencode mcp list            # 列出
opencode mcp auth <server>   # OAuth 认证
opencode mcp logout <server> # 移除凭证
opencode mcp debug <server>  # 调试
```

> ⚠️ **注意**：MCP 服务器会增加 token 消耗。GitHub MCP 这种大型服务器可能轻易吃光上下文。

---

## 10. GitHub 自动化

### 10.1 能干嘛？

在 GitHub Issue 或 PR 下面评论 `/opencode` 或 `/oc`，OpenCode 会自动：

- 分析问题并分类
- 创建分支、写代码、提交 PR
- 做代码审查

### 10.2 一键安装

```bash
opencode github install
```

跟着提示走，它会帮你：
1. 安装 GitHub App
2. 创建 workflow 文件
3. 配置 secrets

### 10.3 手动配置

**第一步**：安装 GitHub App → [github.com/apps/opencode-agent](https://github.com/apps/opencode-agent)

**第二步**：在仓库里加 `.github/workflows/opencode.yml`：

```yaml
name: opencode
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  opencode:
    if: contains(github.event.comment.body, '/oc')
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v6
      - uses: anomalyco/opencode/github@latest
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        with:
          model: anthropic/claude-sonnet-4
```

**第三步**：把 `ANTHROPIC_API_KEY` 加到仓库的 Secrets 里。

---

## 11. IDE 里怎么用

### 11.1 支持的 IDE

VS Code、Cursor、Windsurf、Zed、JetBrains IDEs、Neovim（Avante/CodeCompanion）——几乎所有主流编辑器都支持。

### 11.2 VS Code / Cursor 安装

最简单的方式：

1. 打开 IDE
2. 打开**集成终端**
3. 运行 `opencode`

扩展会自动安装。

### 11.3 快捷键

| 操作 | macOS | Windows/Linux |
|------|-------|--------------|
| 快速启动 | `Cmd+Esc` | `Ctrl+Esc` |
| 新建会话 | `Cmd+Shift+Esc` | `Ctrl+Shift+Esc` |
| 引用文件 | `Cmd+Option+K` | `Alt+Ctrl+K` |

### 11.4 Zed 配置

在 `~/.config/zed/settings.json` 里加：

```json
{
  "external_agents": [
    {
      "command": "opencode",
      "args": ["acp"]
    }
  ]
}
```

然后用 `agent: new thread` 打开。

### 11.5 JetBrains IDEs

在 `acp.json` 里配置，然后在 AI Chat 里选择 **"OpenCode"** agent。

### 11.6 Neovim

**Avante.nvim：**
```lua
require("avante_nvim").setup({
  providers = {
    opencode = {
      command = "opencode",
      args = { "acp" },
    },
  },
})
```

**CodeCompanion.nvim：**
```lua
require("codecompanion").setup({
  adapters = {
    opencode = function()
      return require("codecompanion.adapters").extend("opencode", {
        command = "opencode",
        args = { "acp" },
      })
    end,
  },
})
```

---

## 12. Web 界面

不想用终端？OpenCode 也有网页版。

### 12.1 启动

```bash
opencode web
```

会自动在浏览器里打开。

### 12.2 常用参数

```bash
opencode web --port 4096              # 指定端口
opencode web --hostname 0.0.0.0       # 允许局域网访问
OPENCODE_SERVER_PASSWORD=secret opencode web  # 加密码
```

### 12.3 同时用 Web 和终端

```bash
# 终端 1：启动 Web 服务器
opencode web --port 4096

# 终端 2：附加 TUI 到同一个服务器
opencode attach http://localhost:4096
```

两边共享同一个会话，互不影响。

---

## 13. Hermes 里怎么用 OpenCode

### 13.1 两种模式

**模式 A：一次性任务（推荐用于简单任务）**

```bash
opencode run 'Add retry logic to API calls and update tests'
```

优点：不用管进程，执行完自动退出。

**模式 B：后台交互会话（推荐用于复杂任务）**

```bash
# 启动后台会话
terminal(command="opencode", workdir="~/project", background=True, pty=True)

# 发送消息
process(action="submit", session_id="xxx", data="Implement OAuth flow")

# 看进度
process(action="log", session_id="xxx")

# 退出
process(action="write", session_id="xxx", data="\x03")  # Ctrl+C
```

### 13.2 带上下文的调用

```bash
# 附加文件
opencode run 'Review security' -f config.yaml -f .env.example

# 指定模型
opencode run 'Refactor' --model openrouter/anthropic/claude-sonnet-4

# 显示思考过程
opencode run 'Debug' --thinking
```

### 13.3 PR 审查

```bash
# 方式一：内置命令
opencode pr 42

# 方式二：临时克隆
REVIEW=$(mktemp -d) && \
git clone https://github.com/user/repo.git $REVIEW && \
cd $REVIEW && \
opencode run 'Review this PR vs main' \
  -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')
```

### 13.4 并行任务

```bash
# 用不同目录避免冲突
terminal(command="opencode run 'Fix #101'", workdir="/tmp/issue-101", background=True, pty=True)
terminal(command="opencode run 'Fix #102'", workdir="/tmp/issue-102", background=True, pty=True)
```

---

## 14. 自定义命令和工具

### 14.1 自定义命令——把重复操作变成 `/命令`

**场景**：每次都要跑测试 + 看覆盖率 + 修复失败项，太麻烦。

**做法**：在 `.opencode/commands/test.md` 里写：

```markdown
---
description: 运行测试并修复失败项
agent: build
---

Run the full test suite with coverage report.
Fix any failing tests and explain what was changed.
```

以后直接打 `/test` 就行。

### 14.2 高级用法

**带参数：**
```markdown
---
description: 为组件写测试
---

Write unit tests for @src/components/$1.tsx
```

调用：`/test Button` → `$1` 变成 `Button`

**注入 shell 输出：**
```markdown
---
description: 基于最近提交写 changelog
---

Generate changelog based on recent commits:
!`git log --oneline -10`
```

**引用文件：**
```markdown
---
description: 审查 API 接口
---

Review @src/api/users.ts for security issues.
```

### 14.3 JSON 方式配置

```jsonc
{
  "command": {
    "deploy": {
      "template": "Deploy $1 to $2 environment",
      "description": "Deploy to specified environment",
      "agent": "build"
    }
  }
}
```

### 14.4 自定义工具——让 AI 能调用你的代码

**场景**：有个内部 API 需要调用，AI 不会用。

**做法**：

1. 写个 Python 脚本 `add.py`：
```python
import sys
a, b = map(int, sys.argv[1:])
print(a + b)
```

2. 写个工具定义 `.opencode/tools/math_add.ts`：
```typescript
import { tool } from "@opencode/tools";
import { z } from "zod";

export const math_add = tool({
  description: "Add two numbers",
  parameters: z.object({
    a: z.number(),
    b: z.number(),
  }),
  execute: async ({ a, b }, context) => {
    const { stdout } = await context.bash(`python3 add.py ${a} ${b}`);
    return { result: parseInt(stdout.trim()) };
  },
});
```

现在 AI 就能直接调用 `math_add` 工具了。

---

## 15. Agent Skills

### 15.1 Skill 是啥？

Skill 就是一段**可重用的工作指南**，告诉 AI 怎么做某类任务。类似 Hermes 的 skill，但格式略有不同。

### 15.2 怎么放文件？

为每个技能建一个文件夹，里面放 `SKILL.md`：

| 位置 | 适用范围 |
|------|---------|
| `.opencode/skills/<name>/SKILL.md` | 当前项目 |
| `~/.config/opencode/skills/<name>/SKILL.md` | 所有项目 |
| `.claude/skills/<name>/SKILL.md` | Claude Code 兼容 |

### 15.3 SKILL.md 长啥样？

```markdown
---
name: git-release
description: 创建一致的发布和变更日志
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do
- 从合并的 PR 起草发布说明
- 提议版本号
- 提供可复制的 `gh release create` 命令

## When to use me
准备标记发布时使用。
```

**命名规则**：
- 小写字母 + 数字 + 单个连字符
- 1-64 个字符
- 不能以 `-` 开头或结尾

### 15.4 AI 怎么发现技能？

OpenCode 会自动扫描上面那些位置，把找到的技能列在 `skill` 工具里：

```xml
<available_skills>
  <skill>
    <name>git-release</name>
    <description>创建一致的发布和变更日志</description>
  </skill>
</available_skills>
```

AI 可以通过调用 `skill({ name: "git-release" })` 加载技能内容。

### 15.5 技能权限

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| 权限 | 行为 |
|------|------|
| `allow` | 直接加载 |
| `deny` | 对 AI 隐藏 |
| `ask` | 加载前问你 |

---

## 16. 常见问题

### 16.1 装了但 `opencode` 找不到？

```bash
which -a opencode    # 看所有安装位置
$HOME/.opencode/bin/opencode --version  # 用完整路径
```

可能是 PATH 没配好。把 `~/.opencode/bin` 加到 PATH：

```bash
export PATH="$HOME/.opencode/bin:$PATH"
```

### 16.2 TUI 卡住了怎么办？

**不要直接 kill！** 先看看日志：

```bash
process(action="log", session_id="xxx")
```

然后发中断信号：

```bash
process(action="write", session_id="xxx", data="\x03")  # Ctrl+C
```

实在不行再 kill。

### 16.3 模型报错 / 认证失败？

```bash
opencode auth list        # 看哪些 Key 配了
opencode models --refresh # 刷新模型列表
opencode models --verbose # 看模型详情
```

### 16.4 权限不够，AI 不能改文件？

检查 `opencode.json`：

```bash
cat opencode.json | grep -A5 '"permission"'
```

确保 `edit` 权限是 `allow` 或 `ask`。

### 16.5 上下文超限了？

- 用 `/compact` 压缩上下文
- 减少附加文件数量
- 关掉不用的 MCP 服务器
- 简单任务用 `small_model`

### 16.6 Smoke 测试（验证一切正常）

```bash
opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'
```

应该输出 `OPENCODE_SMOKE_OK`。

---

## 17. OpenCode vs Claude Code

### 17.1 核心差异

| 维度 | OpenCode | Claude Code |
|------|----------|-------------|
| **开源** | ✅ 完全开源 | ❌ 闭源 |
| **模型选择** | 75+ 提供商 | 仅限 Claude |
| **本地模型** | ✅ 支持 | ❌ 不支持 |
| **桌面应用** | ✅ Beta | ✅ |
| **IDE 集成** | ✅ | ✅ |
| **价格** | API 按量付费 | Claude Pro $20/月 |
| **GitHub stars** | 160K+ | 71K+ |
| **LSP 集成** | ✅ 自动 | ✅ |
| **多会话并行** | ✅ | ✅ |
| **MCP 支持** | ✅ | ✅ |

### 17.2 怎么选？

**选 OpenCode**：
- 想要模型自由，随时换
- 需要本地 LLM（Ollama 等）
- 想要完全开源，可 fork 修改
- 预算有限，想用免费模型
- 需要跨平台桌面应用

**选 Claude Code**：
- 想最快上手，不想折腾配置
- 需要最强的复杂推理能力
- 已经在 Anthropic 生态里（有 Claude Pro）
- 需要生产环境验证过的工具
- 不介意被锁定在 Claude 模型

### 17.3 重要事件

**2026 年 1 月**：Anthropic 阻止 OpenCode 使用 Claude 模型（OAuth 限制）。这反而推动了 OpenCode 的多模型适配发展——现在用 GPT、Gemini、本地模型的用户更多了。

---

## 18. 企业怎么用

### 18.1 数据安全吗？

**OpenCode 不存储你的代码或上下文数据。** 所有处理在本地完成，或者直连你的 AI 提供商 API。

唯一例外是 `/share` 功能——会把对话发到 opencode.ai。企业环境建议禁用。

### 18.2 企业版有什么？

| 功能 | 说明 |
|------|------|
| 集中式配置 | 全公司统一配置，远程下发 |
| SSO 集成 | 用公司账号登录 |
| 内部 AI 网关 | 所有请求走公司内部网关 |
| 禁用分享 | 强制关闭 `/share` |
| 私有 NPM 注册表 | 支持公司私有包 |
| 按席位定价 | 有自己的 LLM 网关时不收 token 费 |

### 18.3 私有 NPM 注册表怎么配？

```bash
echo "//registry.example.com/:_authToken=${NPM_TOKEN}" > ~/.npmrc
```

OpenCode 会自动读取。

### 18.4 安全建议

1. 试用期间禁用 `/share`
2. 用集中式配置强制走内部 AI 网关
3. 集成 SSO 统一认证
4. 敏感项目完全禁用分享功能

---

## 19. 插件和生态

### 19.1 插件是啥？

插件用 JS/TS 写，可以**挂钩 OpenCode 的各种事件**，比如：
- 文件被修改了
- 会话创建了
- 工具要执行了
- TUI 要显示内容了

### 19.2 怎么加载插件？

**本地文件：**
- `.opencode/plugins/`（项目级）
- `~/.config/opencode/plugins/`（全局）

**npm 包：**
```json
{
  "plugin": ["opencode-helicone-session", "@my-org/custom-plugin"]
}
```

### 19.3 有哪些热门插件？

| 插件 | 功能 |
|------|------|
| `opencode-daytona` | 用 Daytona sandbox 隔离会话 |
| `opencode-helicone-session` | Helicone 会话头注入 |
| `opencode-type-inject` | TypeScript/Svelte 类型自动注入 |
| `opencode-openai-codex-auth` | 用 ChatGPT Plus 订阅而非 API |
| `opencode-gemini-auth` | 用 Gemini 计划而非 API 计费 |
| `opencode-vibeguard` | LLM 前脱敏 secrets/PII |
| `opencode-morph-fast-apply` | **10x 更快代码编辑** |
| `opencode-supermemory` | 跨会话持久记忆 |
| `opencode-scheduler` | launchd/systemd 作业调度 |
| `opencode-conductor` | Context → Spec → Plan → Implement 自动化 |
| `opencode-background-agents` | Claude Code 风格后台代理 |
| `opencode-workspace` | 多代理编排（16 组件） |
| `opencode-sentry-monitor` | Sentry 错误监控 |

### 19.4 怎么写插件？

```javascript
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    hooks: {
      "file.edited": async ({ event }) => {
        console.log("文件被修改了:", event.path);
      },
      "session.created": async ({ event }) => {
        console.log("新会话创建了:", event.sessionId);
      }
    }
  };
};
```

更多事件类型：Command、File、Session、Tool、TUI 等 10+ 类别。

### 19.5 社区资源

- [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) — 精选资源列表
- [opencode.cafe](https://opencode.cafe) — 社区聚合

---

## 20. SDK 开发

### 20.1 Python SDK

```python
from opencode import OpenCodeClient

client = OpenCodeClient()
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Explain closures in JS"}]
)
print(response.choices[0].message.content)
```

### 20.2 TypeScript SDK

```typescript
import { OpenCodeClient } from "@opencode/client";

const client = new OpenCodeClient();
const response = await client.chat.completions.create({
  model: "anthropic/claude-sonnet-4",
  messages: [{ role: "user", content: "Explain closures in JS" }]
});
console.log(response.choices[0].message.content);
```

---

## 21. 附录：wiki 知识库索引

本手册内容来源于 `~/wiki/opencode/` 以下文件：

### Entities（实体文档，21 个）

| 文件 | 对应章节 |
|------|----------|
| `opencode.md` | §1 简介 |
| `opencode-installation.md` | §2 安装 |
| `opencode-configuration.md` | §3 配置 |
| `opencode-cli-commands.md` | §4 命令 |
| `opencode-tui.md` | §5 TUI |
| `opencode-models.md` | §6 模型 |
| `opencode-agents.md` | §7 代理 |
| `opencode-tools.md` | §8 工具 |
| `opencode-mcp.md` | §9 MCP |
| `opencode-github.md` | §10 GitHub |
| `opencode-vs-claude-code.md` | §17 对比 |
| `opencode-permissions.md` | §8 权限 |
| `opencode-lsp.md` | §8 LSP |
| `opencode-sdk.md` | §20 SDK |
| `opencode-enterprise.md` | §18 企业 |
| `opencode-share.md` | §5.7 分享 |
| `opencode-ecosystem.md` | §19 生态 |
| `opencode-rules.md` | §3.5 规则 |
| `opencode-plugins.md` | §19 插件 |
| `opencode-commands.md` | §14 自定义命令 |
| `opencode-ide-integration.md` | §11 IDE |

### Concepts（概念文档，19 个）

| 文件 | 对应章节 |
|------|----------|
| `opencode-configuration-guide.md` | §3 配置详解 |
| `opencode-tui-guide.md` | §5 TUI 详解 |
| `opencode-agents-guide.md` | §7 代理指南 |
| `opencode-models-providers.md` | §6 模型提供商 |
| `opencode-mcp-integration.md` | §9 MCP 集成 |
| `opencode-github-integration.md` | §10 GitHub 集成 |
| `opencode-custom-commands.md` | §14 自定义命令 |
| `opencode-custom-tools.md` | §14 自定义工具 |
| `opencode-acp-support.md` | §11 ACP |
| `opencode-web-interface.md` | §12 Web |
| `opencode-session-sharing.md` | §5.7 分享 |
| `opencode-agent-skills.md` | §15 Agent Skills |
| `opencode-ecosystem-overview.md` | §19 生态概览 |
| `opencode-plugins-guide.md` | §19 插件指南 |
| `opencode-installation-quickstart.md` | §2 快速开始 |
| `opencode-enterprise-deployment.md` | §18 企业部署 |
| `opencode-sdk-usage.md` | §20 SDK 使用 |
| `opencode-ide-integration.md` | §11 IDE 集成 |
| `opencode-custom-tools.md` | §14 自定义工具 |

### Raw Articles（原始文章，37 个）

位于 `~/wiki/raw/articles/`，为上述文档的原始 Markdown 来源。

---

> **使用建议**：本手册为操作参考，实际使用时建议结合 `skill_view(name='opencode')` 获取 Hermes 集成的具体命令模板。wiki 知识库路径为 `~/wiki/opencode/`，可通过 `skill_view(name='llm-wiki')` 学习如何查询和扩展 wiki。
