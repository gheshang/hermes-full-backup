# Plan: 爬取 Hermes 官方文档入 Wiki + 优化配置脚本

## Goal
1. 将 Hermes 官方 GitHub 仓库 224 篇未入库文档批量爬入 `~/.hermes/wiki/`
2. 基于官方文档中新发现的功能点，优化 `~/.hermes/hermes_setup_all.py`，增加省 token / 高效 / 实用的新功能项
3. 查询社区开源方案，吸收进脚本

## Current Context

### 已有资产
- **Wiki**: 31 页已收录（29 篇与官方文档对应），域定义为 AI Agent 技术栈
- **Wiki Schema**: `~/.hermes/wiki/SCHEMA.md` — frontmatter 规范、tag 体系、page threshold
- **Ingest 脚本**: `~/.hermes/scripts/wiki_ingest.py` — 支持 GitHub raw / Docusaurus 自动发现 / curl / web_extract / 浏览器 五级策略，自动 raw→wiki page→index→log→git push
- **配置脚本**: `~/.hermes/hermes_setup_all.py` — 12 大项三层架构（核心配置/Token优化/进阶功能），刚完成 token + setup 合并
- **Skills**: `hermes-config-setup` + `hermes-token-optimization` 两个 skill 均指向合并后的单脚本

### 官方文档全貌（253 .md，224 未入库）
GitHub: `NousResearch/hermes-agent`，路径 `website/docs/`
目录结构：
- `getting-started/` (5) — installation, quickstart, learning-path, nix-setup, termux, updating
- `guides/` (14) — tips, automate-with-cron, automation-templates, delegation-patterns, build-a-hermes-plugin, use-mcp, use-soul, voice-mode, webhook-github-pr-review, work-with-skills, daily-briefing-bot, github-pr-review-agent, local-llm-on-mac, python-library, aws-bedrock, migrate-from-openclaw, cron-troubleshooting
- `reference/` (9) — cli-commands, environment-variables, faq, mcp-config, optional-skills-catalog, profile-commands, skills-catalog, slash-commands, tools-reference, toolsets-reference
- `user-guide/` (20+features, 16+messaging, 4+skills) — configuration, cli, docker, profiles, security, sessions, git-worktrees, tui
  - `features/` (28): overview, tools, skills, memory, context-files, context-references, credential-pools, cron, delegation, fallback-providers, hooks, provider-routing, browser, vision, tts, voice-mode, image-generation, plugins, personality, skins, batch-processing, code-execution, honcho, memory-providers, tool-gateway, web-dashboard, rl-training, dashboard-plugins, acp, api-server, built-in-plugins
  - `messaging/` (16): telegram, discord, slack, weixin, wecom, wecom-callback, feishu, dingtalk, signal, sms, matrix, email, whatsapp, homeassistant, webhooks, open-webui, bluebubbles, mattermost, qqbot
- `developer-guide/` (20): architecture, agent-loop, prompt-assembly, context-compression-and-caching, context-engine-plugin, provider-runtime, tools-runtime, cron-internals, gateway-internals, session-storage, browser-supervisor, environments, contributing, creating-skills, adding-tools, adding-providers, adding-platform-adapters, extending-the-cli, memory-provider-plugin, trajectory-format
- `integrations/` (2): index, providers

### 已读取的高价值文档（新发现的功能点）

| 文档 | 脚本当前覆盖 | 新发现可优化点 |
|------|-------------|---------------|
| **credential-pools.md** | ✅ feat4（密钥池策略） | 补充 `random` 策略；补充 `hermes auth` 交互向导命令；补充 OAuth 类型凭证 |
| **provider-routing.md** | ❌ 无 | **新增功能项**：OpenRouter 下的 provider_routing（sort/only/ignore/order/data_collection） |
| **fallback-providers.md** | ❌ 无 | **新增功能项**：fallback_model 配置（跨 provider 自动故障切换） |
| **context-compression-and-caching.md** | ✅ feat6（压缩） | 补充 `context.engine` 可替换为 LCM 等插件引擎；补充双压缩系统说明（Gateway 85% + Agent 50%） |
| **configuration.md** | ✅ 部分 | 补充 `hermes config set` 自动路由 API key 到 .env 的能力；补充 `${VAR}` 环境变量替换；补充 provider timeouts |
| **delegation.md** | ✅ feat10 | 补充 `max_spawn_depth` 配置；orchestrator vs leaf 角色说明 |
| **hooks.md** | ❌ 无 | **新增功能项**：shell hooks（config.yaml 里绑脚本）、gateway hooks |
| **environment-variables.md** | ❌ 无 | 可作参考页，不需脚本配 |
| **context-files.md** | ❌ 无 | **新增功能项**：AGENTS.md / .hermes.md 自动发现机制配置 |
| **batch-processing.md** | ❌ 无 | 低优先级，批量跑 agent 生成训练数据，普通用户不需要 |
| **tool-gateway.md** | ❌ 无 | **新增功能项**：Nous Tool Gateway（付费用户免额外 API key 用搜索/图片/TTS/浏览器） |
| **personality.md** | ❌ 无 | 低优先级，SOUL.md 已存在 |

## Proposed Approach

### Phase 1: 批量爬取官方文档入 Wiki

**方案**: 直接使用 `wiki_ingest.py --github NousResearch/hermes-agent --docs-path website/docs` 一次拉全部。

**分批策略**（避免超时/限流）:
1. **核心配置相关**（优先级最高，与脚本优化直接相关）：`user-guide/configuration.md`, `user-guide/features/` 全部, `reference/` 全部, `integrations/providers.md` ≈ 40 篇
2. **进阶指南**：`guides/` 全部 ≈ 17 篇
3. **消息平台**：`user-guide/messaging/` 全部 ≈ 18 篇
4. **开发指南**：`developer-guide/` 全部 ≈ 20 篇
5. **Skill 文档**：`user-guide/skills/` 全部 ≈ 149 篇（这些内容已有 skill 本身，低优先级，可选跳过）

**执行方式**: 
```bash
# 方案A：wiki_ingest.py 批量模式（推荐，已有现成脚本）
python3 ~/.hermes/scripts/wiki_ingest.py https://hermes-agent.nousresearch.com \
  --github NousResearch/hermes-agent \
  --docs-path website/docs/user-guide/features \
  --docs-path website/docs/reference \
  --docs-path website/docs/guides

# 方案B：手动 curl + 写入 raw/（如果 wiki_ingest.py 有兼容问题）
# 用 execute_code 批量拉取
```

**注意事项**:
- `wiki_ingest.py` 依赖 `shell=True` 的 `run_cmd()`，需确认不会因 URL 中的特殊字符出问题
- GitHub API 有 60 req/hr 限制（未认证），253 文件需分批或用 authenticated curl
- wiki_ingest.py 生成 wiki 页时需要做 frontmatter 格式化，确认与 SCHEMA.md 一致
- skill 文档（149 篇）已有 skill 本身，建议 `--raw-only` 只存 raw 不生成 wiki 页

### Phase 2: 优化配置脚本（基于官方文档新发现）

新增 **4 个功能项**，调整 **3 个现有功能项**：

#### 新增功能项

| # | 功能 | 来源 | 配置项 |
|---|------|------|--------|
| 13 | **Provider Routing** | provider-routing.md | `provider_routing.sort` / `.only` / `.ignore` / `.order` / `.data_collection` / `.require_parameters` |
| 14 | **Fallback Provider** | fallback-providers.md | `fallback_model.provider` + `fallback_model.model` |
| 15 | **Shell Hooks** | hooks.md | `hooks.pre_tool` / `hooks.post_tool` / `hooks.on_session_start` 等 |
| 16 | **Nous Tool Gateway** | tool-gateway.md | `hermes status` 检查 → 启用 web/image/tts/browser 四件套 |

#### 调整现有功能项

| # | 功能 | 调整内容 |
|---|------|----------|
| 4 | 密钥池策略 | 补充 `random` 策略选项；引导 `hermes auth` 交互向导；补充 OAuth 凭证类型说明 |
| 6 | 上下文压缩 | 补充 `context.engine` 可替换（compressor/lcm/插件）；说明双压缩阈值（Gateway 85% vs Agent 50%）；compression 默认值校准为官方 0.50（而非之前知乎的 0.75） |
| 10 | 子 Agent 并发 | 补充 `delegation.max_spawn_depth` 配置；说明 orchestrator vs leaf 角色 |

#### 不新增但需文档化的
- `hermes config set` 自动路由 API key 到 .env（已在 feat1/feat2 中隐含使用，但未显式告知用户这个特性）
- `${VAR}` 环境变量替换（config.yaml 支持引用 .env 变量）
- provider timeouts（`providers.<name>.request_timeout_seconds` 等）

### Phase 3: 查询社区开源方案

**目标**: 找到非官方的省钱技巧 / 优化配置 / 实用脚本

**搜索方向**:
1. Reddit r/hermesagent — high token consumption 讨论帖（已有 URL）
2. YouTube "85% token save" 视频（已有 URL，需提取内容）
3. GitHub `hermes-optimization-guide` 仓库（已有 URL: OnlyTerp/hermes-optimization-guide）
4. 中文社区（知乎/SegmentFault）的进阶用法文章

**筛选标准**: 只吸收可脚本化、可配置化的技巧，不吸收纯操作建议（如"用更便宜的模型"）

## Step-by-Step Plan

### Step 1: 爬取核心文档入 Wiki（40 篇）
```bash
python3 ~/.hermes/scripts/wiki_ingest.py \
  https://hermes-agent.nousresearch.com/docs/user-guide/features \
  --github NousResearch/hermes-agent \
  --docs-path website/docs/user-guide/features
```
同样拉 `reference/`、`guides/`、`integrations/providers.md`、`user-guide/configuration.md`

### Step 2: 爬取消息平台 + 开发指南文档（38 篇）
```bash
python3 ~/.hermes/scripts/wiki_ingest.py \
  --github NousResearch/hermes-agent \
  --docs-path website/docs/user-guide/messaging \
  --docs-path website/docs/developer-guide
```

### Step 3: Skill 文档 raw-only 存档（149 篇，可选）
```bash
python3 ~/.hermes/scripts/wiki_ingest.py \
  --github NousResearch/hermes-agent \
  --docs-path website/docs/user-guide/skills \
  --raw-only
```

### Step 4: 查询社区方案
- 提取 YouTube 视频内容（用 youtube-content skill）
- 爬取 Reddit 讨论帖
- 爬取 OnlyTerp/hermes-optimization-guide
- 搜索中文社区文章

### Step 5: 优化 hermes_setup_all.py
- 新增 feat13~feat16 四个功能项
- 调整 feat4/feat6/feat10
- 更新菜单（三层→四层或保持三层扩展项数）
- 代码复核

### Step 6: 更新 skills
- patch `hermes-config-setup` SKILL.md — 新增功能项说明
- patch `hermes-token-optimization` SKILL.md — 补充双压缩系统说明
- 更新 wiki index.md

## Files Likely to Change

| File | Action |
|------|--------|
| `~/.hermes/hermes_setup_all.py` | 新增4个feat函数 + 调整3个现有feat + 菜单更新 |
| `~/.hermes/skills/devops/hermes-config-setup/SKILL.md` | 更新功能列表、合并说明 |
| `~/.hermes/skills/devops/hermes-token-optimization/SKILL.md` | 补充双压缩系统、context.engine 说明 |
| `~/.hermes/wiki/` (raw/ + concepts/ + entities/) | 40-80 新 wiki 页面 |
| `~/.hermes/wiki/index.md` | 更新索引 |
| `~/.hermes/wiki/log.md` | 记录爬取操作 |

## Tests / Validation

1. **Wiki 爬取验证**: `find ~/.hermes/wiki/ -name "*.md" -not -path "*/.git/*" | wc -l` — 应从 ~40 增至 ~80+
2. **Wiki 链接验证**: 抽查 5 篇新页面的 frontmatter 和 `[[wikilinks]]`
3. **脚本语法验证**: `python3 -c "import ast; ast.parse(open('~/.hermes/hermes_setup_all.py').read())"` 
4. **脚本逻辑验证**: 每个新 feat 函数的输入→配置写入→.env 写入 闭环
5. **安全验证**: 无 `shell=True`，API key 不进 config.yaml，.env 权限 0600

## Risks, Tradeoffs, and Open Questions

### Risks
1. **GitHub API 限流**: 未认证 60 req/hr，253 文件需 ~4.5 小时分批拉完。**缓解**: 用 `GITHUB_TOKEN` 认证提升至 5000 req/hr
2. **wiki_ingest.py 兼容性**: 脚本用 `shell=True` 执行 curl，URL 含特殊字符时可能出问题。**缓解**: 先 dry-run 测试
3. **脚本膨胀**: 12→16 功能项，交互流程过长。**缓解**: 保持可选机制，默认只推荐核心项

### Tradeoffs
- **全量爬取 vs 精选爬取**: Skill 文档 149 篇，内容与已有 skill 高度重复。选择 raw-only 存档，不生成 wiki 页
- **知乎默认值 vs 官方默认值**: compression.threshold 官方默认 0.50，知乎建议 0.75。按官方默认，但保留用户可调

### Open Questions
1. **provider_routing 只对 OpenRouter 有效**——是否需要明确提示用户"非 OpenRouter 用户可跳过"？
2. **Nous Tool Gateway 需付费订阅**——是否在脚本里直接引导用户去订阅？还是只做检测提示？
3. **context.engine 插件（LCM）**——目前 Hermes 社区是否有成熟的 LCM 插件可安装？还是纯配置预留？
