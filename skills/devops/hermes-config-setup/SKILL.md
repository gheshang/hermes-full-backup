---
name: hermes-config-setup
description: 交互式脚本引导用户配置 Hermes Agent 的副驾模型、搜索后端、记忆系统、进阶功能（Profile/Skill进化/并发/Cron/Token监控/生态工具），支持自定义厂商(base_url+api_key)，API Key 写 .env 而非 config.yaml。
version: 5.0
metadata:
 hermes:
 tags: [hermes, config, auxiliary, search, memory, security, profile, cron, token]
 related_skills: [karpathy-coding-guidelines, agency-agents-zh]
---

# Hermes Agent 配置引导脚本

## 触发条件

用户要求配置 Hermes Agent 的任何功能，包括：副驾模型、搜索后端、记忆系统、Profile 分身、Skill 进化、子 Agent 并发、Cron 定时、Token 监控与压缩、生态工具。

## 合并说明

本 skill 已与 `hermes-token-optimization` 合并为单一脚本 `~/.hermes/hermes_setup_all.py`。
16 大项可选，四层架构：核心配置(1-3) → Token 优化(4-7) → 成本控制(13-16) → 进阶功能(8-12)。
基于官方文档（253篇）+ 社区优化方案（OnlyTerp/hermes-optimization-guide）持续迭代。
旧脚本 `~/.hermes/hermes_token_optimizer.py` 已删除。

## 交互式脚本运行限制

Hermes 的 terminal 工具无法运行需要用户交互输入（`input()`）的 Python 脚本——pty 模式下 `input()` 会收到 EOF 导致 `EOFError`。

交互式脚本必须让用户在本地终端手动运行：
```bash
python3 ~/.hermes/hermes_setup_all.py
```

替代方案：用户把配置信息（厂商、模型、API Key 等）直接告诉 Hermes，由 Hermes 后台用 `hermes config set` 一条条配——但注意 API Key 会留在对话记录中，存在泄露风险。

---

## 16 项配置详解

每项包含：配置了会怎样 → 不配会怎样 → 具体操作步骤 → 验证方法

### 1. 副驾模型（auxiliary）

**不配**：所有副驾任务（vision/compression/session_search/approval/skills_hub/mcp/web_extract/flush_memories）走主模型。相当于用 GLM-5 去干正则匹配的活，每次 vision 调用花主模型价钱的 token，成本翻 3-5 倍。

**配了**：重任务用稍强模型（如 gemini-2.5-flash），轻任务用便宜快模型（如 gemini-2.5-flash-lite），成本降 60-70%。

**具体步骤**：
1. 选批量配(a)或逐任务配(b)
2. 批量模式（推荐）：
   - 重任务模型：填 provider(如 custom) + model(如 gemini-2.5-flash) + base_url(custom必填) + API key
   - 轻任务模型：填 provider + model(如 gemini-2.5-flash-lite) + base_url + API key
   - 重任务覆盖：vision, web_extract, flush_memories
   - 轻任务覆盖：compression, session_search, approval, skills_hub, mcp
3. 逐任务模式：逐个填每个副驾任务的 provider/model/base_url/timeout/API key
4. API key 写入 `~/.hermes/.env`（权限 0600），config.yaml 只存环境变量名

**验证**：`hermes config | grep auxiliary`，确认每个任务的 provider/model 非空

---

### 2. 搜索后端

**不配**：`web_search` 工具报错或返回空结果，无法联网搜索，只能靠模型自身知识（截止训练日期）。

**配了**：
- tavily：专为 AI 设计的结构化搜索结果，月 1000 次免费额度，质量最高
- duckduckgo：零成本无限次，不需 API key，但结果无结构化处理，质量略低

**具体步骤**：
1. 选 tavily(1) 或 duckduckgo(2)
2. tavily：去 tavily.com 注册拿 API key → 填入 → 写入 .env → config 设 `web.tavily_api_key_env=TAVILY_API_KEY`
3. config 设 `web.backend=tavily` + `web.fallback_backend=duckduckgo`（建议配兜底）
4. duckduckgo：直接设 `web.backend=duckduckgo`，无需 key

**验证**：`hermes config get web.backend`，然后让 Hermes 搜个东西试试

---

### 3. 记忆系统

**不配**：每次对话都是失忆状态，上轮说过的偏好/项目信息/踩坑经验下轮全部重来。每轮花额外 token 重复交代背景。

**配了**：跨会话记住用户偏好、项目信息、踩坑经验，减少重复沟通。内置记忆默认已开。

**具体步骤**：
1. 内置记忆默认已开启，一般不需手动配
2. 可调参数：
   - `memory.memory_char_limit`：MEMORY.md 上限字符数，默认 2200，超了触发压缩/淘汰
   - `memory.user_char_limit`：USER.md 上限字符数，默认 1375
   - `memory.nudge_interval`：每 N 轮提醒 agent 存记忆，默认 10
   - `memory.flush_min_turns`：至少 N 轮才触发退出时刷新记忆到文件，默认 6
3. 外部 Memory Provider（可选）：支持 honcho/mem0/hindsight 等，建议先跑两周内置记忆再决定是否上外部 provider
4. 外部 provider 配置：`hermes memory setup`（交互向导）

**验证**：`hermes config | grep memory`，确认 `memory_enabled=true`

---

### 4. 密钥池策略（credential_pool）

**不配**：单个 API key 打到速率限制就报 429，对话中断，前面花的所有 token 白费。

**配了**：同 provider 多 key 轮转，一个 key 限流自动切下一个，不中断对话。

**具体步骤**：
1. 选要配的 provider（如 zai）
2. 选策略：
   - `least_used`（推荐）：始终选请求量最少的 key，均衡负载
   - `round_robin`：轮询循环
   - `fill_first`：用完一个再用下一个，不均衡
   - `random`：随机选择
3. 添加密钥到池：
   - 方式A：`hermes auth`（交互向导，推荐）
   - 方式B：手动逐个添加 API key 到 .env，然后 `hermes auth add` seed 到池
4. 支持 OAuth 类型凭证（如 Anthropic OAuth）：`hermes auth add <provider> --type oauth`

**验证**：`hermes auth list`，确认池中有多个 key

---

### 5. 上下文窗口 & 最大输出

**不配**：压缩算法无法精准计算触发时机（不知道窗口多大），可能过早压缩浪费 token，也可能过晚压缩直接爆窗口。`max_tokens` 不设则模型输出可能被截断。

**配了**：压缩算法精确知道何时触发，模型输出不会被截断。

**具体步骤**：
1. `context_length`：填模型上下文窗口 token 数（查模型文档）
   - GLM-5 = 200000, Claude Sonnet = 200000, GPT-4o = 128000
2. `max_tokens`：填模型最大输出 token 数
   - GLM-5 = 131072, Claude Sonnet = 16384, GPT-4o = 16384
3. 不确定的值宁可填大不填小，填小了会过早压缩

**验证**：`hermes config get model.context_length; hermes config get model.max_tokens`

---

### 6. 上下文压缩（双系统 + 引擎可替换）

**不配**：对话太长后直接爆窗口报错，前面的内容全丢，只能开新对话重来。

**配了**：达阈值自动压缩旧内容，保留最近 N 条消息不压缩，对话可以无限延续。双压缩层：Gateway 安全网（85%阈值，不可配）+ Agent 主压缩（50%阈值，可调）。

**具体步骤**：
1. 确保 `compression.enabled=true`
2. 选引擎：
   - `compressor`（默认）：有损总结，用便宜模型压缩上下文
   - `lcm`：无损上下文管理，需安装 context-engine-plugin
   - 其他第三方插件
3. 调参数：
   - `threshold`：0.75 = 上下文占用 75% 时触发压缩（官方默认 0.50 太激进，0.75 更稳）
   - `target_ratio`：0.25 = 压缩后保留 25% 原文内容
   - `protect_last_n`：30 = 保护最近 30 条消息不参与压缩
4. 可选配便宜模型做压缩总结（`compression.summary_provider/model`），主模型省 10 倍

**验证**：`hermes config | grep compression`，然后长对话测一下触发压缩是否正常

---

### 7. Token 监控工具

**不配**：不知道 token 花在哪，终端命令输出吃大量输入 token（ls -la 之类的长输出直接灌进上下文）。

**配了**：tokscale 一条命令看全局消耗；hermes-dashboard 按组件拆解；RTK 把终端命令 token 压掉 80-90%。

**具体步骤**：
1. 监控工具三选一：
   - tokscale：`pip install tokscale`，使用 `tokscale --hermes`
   - hermes-dashboard：`pip install hermes-dashboard`，使用 `hermes-dashboard`
   - hermes dashboard（官方 Web UI）：`hermes dashboard`（必须后台启动，否则 30s 超时被杀）
2. RTK（Rust Token Killer）：`cargo install rtk` → `hermes config set terminal.compressor rtk`
   - 效果：终端命令输出 token 压掉 80-90%
   - 前置：需要 cargo（Rust 包管理器）

**验证**：`tokscale --hermes` 或 `hermes dashboard`

---

### 8. Profile 分身

**不配**：工作/个人/实验混在一个配置里，改一个影响全局。换了主模型连记忆都跟着变。

**配了**：每个分身独立记忆/人格/配置，互不干扰，随时切换。

**具体步骤**：
1. 填 Profile 名称（只允许字母、数字、连字符、下划线，不能有空格）
   - 常用名：work / life / coder / experiment
2. 选是否从当前配置克隆（推荐 y，否则空白分身需重新配所有东西）
3. 可选设为默认 Profile
4. 日常管理：
   - `hermes profile list`：查看所有分身
   - `hermes -p <name> chat`：临时切换（下次启动恢复默认）
   - `hermes profile use <name>`：粘性切换为默认
   - `hermes profile delete <name>`：删除

**验证**：`hermes profile list`，确认分身存在

---

### 9. Skill 自主进化

**不配**：每次踩同样的坑都要重新教，重复操作无法沉淀为可复用流程。

**配了**：每 N 次工具调用后台自动审查对话，发现非平凡经验自动沉淀为新 skill 或更新已有 skill，不打断当前对话。

**具体步骤**：
1. 填 `creation_nudge_interval`（默认 15）
   - 15 = 每 15 次工具调用触发一次后台审查
   - 0 = 关闭自主进化
   - 值越小审查越频繁，token 消耗越高
2. 审查机制：达阈值 → fork review agent → 审查对话有无非平凡经验 → 结果三种：
   - `update`：更新已有 skill
   - `create`：新建 skill（打印 `Skill created: xxx`）
   - `nothing`：无新经验，不操作
3. 手动装 skill：`hermes skills install wondelai/skills`（380+跨平台）/ `hermes skills install <owner/repo>`

**验证**：`hermes config get creation_nudge_interval`，然后正常干活观察是否自动 create skill

---

### 10. 子 Agent 并发

**不配**：只能串行干活，3 个独立任务要等 3 倍时间。

**配了**：派多路 agent 同时干活，结果合并返回。v0.11.0 新增 orchestrator 角色可再 spawn 自己的 worker（嵌套调度）。

**具体步骤**：
1. `delegation.max_concurrent_children`：最大并发子 agent 数，建议 2-3（太大会打爆 API 限流）
2. `delegation.max_spawn_depth`：orchestrator 最多嵌套几层，默认 2（防止无限递归）
3. 使用：直接跟 Hermes 说"帮我派 3 路 agent，一个查 A、一个查 B、一个查 C"
4. 注意：子 agent 不继承上下文，指令要在一次请求里塞够，不能追问

**验证**：`hermes config | grep delegation`，然后实际派一个多路任务试试

---

### 11. Cron 定时任务

**不配**：人不在时任务没人跑，每天重复的事每次手动触发。

**配了**：定时自动执行，结果推送到飞书/微信/Telegram 等。

**具体步骤**：
1. **前置条件**：`hermes gateway` 必须在跑，cron 才会按时触发
2. 填 cron 表达式（如 `0 8 * * *` = 每天早8点）或自然语言（如 `every 2h`）
3. 填任务指令（要自包含，cron 运行时无上下文）
4. 选结果推送目标：feishu / weixin / telegram / local（仅保存到文件）
5. 管理命令：
   - `hermes cron list`：查看所有定时任务
   - `hermes cron pause <id>`：暂停
   - `hermes cron resume <id>`：恢复
   - `hermes cron remove <id>`：删除

**验证**：`hermes cron list`，确认任务存在且 next_run_at 在合理范围内

---

### 12. 生态工具

**不配**：技能库少，文档格式转换能力弱，只能处理纯文本。

**配了**：380+ 跨平台 skill（社区）/ 万能格式转换（PDF/DOCX/HTML/EPUB → Markdown）/ Marker 转 PDF 效果优于 Pandoc。

**具体步骤**：
1. Skill 库（按需装，不是全装）：
   - wondelai/skills：380+ 跨平台 skill → `hermes skills install wondelai/skills`
   - awesome-agent-skills：1000+ 社区合集 → `hermes skills install nicholasgriffintn/awesome-agent-skills`
2. 文档处理工具（按需装）：
   - Pandoc：`sudo apt-get install -y pandoc`，万能格式转换
   - Marker：`pip install marker-pdf`，PDF → Markdown 效果优于 Pandoc
3. 生态导航：
   - awesome-hermes-agent: https://github.com/awesome-hermes-agent
   - 生态地图: https://hermes-ecosystem.vercel.app
   - OnlyTerp/hermes-optimization-guide: 21 章优化指南 + 13 个 skill + 5 套配置模板

**验证**：`hermes skills list`，确认新 skill 出现在列表中

---

### 13. Provider Routing（OpenRouter 专用）

**不配**：OpenRouter 默认路由不省钱，可能走贵的底层 provider，同样的模型别人花 $0.5 你花 $2。

**配了**：控制请求路由到最便宜的 provider，禁止用你的数据训练，效果立竿见影。

**⚠️ 仅在使用 OpenRouter 时生效，直连 provider 无效。**

**具体步骤**：
1. `sort`：路由策略
   - `price`（推荐）：最便宜的 provider 优先
   - `throughput`：吞吐量最大的优先
   - `latency`：首 token 延迟最低的优先
2. `only`：白名单 provider（逗号分隔，如 `Anthropic,Google`）
3. `ignore`：黑名单 provider（逗号分隔，如 `Together,DeepInfra`）
4. `data_collection=deny`：禁止用你的数据训练（强烈建议开）
5. `require_parameters=true`：只用支持所有参数的 provider
6. 快捷方式：模型名后加 `:nitro` 启用 throughput 排序

**验证**：`hermes config | grep provider_routing`

---

### 14. Fallback Provider（跨 provider 容灾）

**不配**：主模型 429 限流 / 402 账单 / 401 认证 / 超时时对话直接挂掉，前面花的所有 token 白费，只能重新来。

**配了**：主模型挂了自动切到备用 provider，不丢对话上下文，三层容灾：密钥池(同 provider 轮转) → fallback_model(跨 provider 切换)。

**具体步骤**：
1. 填 fallback provider（如 openrouter/anthropic/custom）+ model
2. custom 需填 base_url + API key（key 写 .env）
3. 触发场景：
   - 429 限流 → 同 key 重试一次 → 失败切 fallback
   - 402 账单 → 立即切 fallback（24h 冷却）
   - 401 认证 → 尝试刷新 → 失败切 fallback
   - 超时/断连 → 切 fallback

**验证**：`hermes config | grep fallback`，故意用错主模型 key 看是否自动切换

---

### 15. Shell Hooks（生命周期钩子）

**不配**：无法在工具调用/会话开始结束等生命周期事件上挂自定义逻辑，每次都要手动做安全检查/格式化/日志。

**配了**：每次工具调用前后/会话开始结束时自动执行你的脚本，可做安全检查、代码格式化、操作日志记录等，零额外 token 开销。

**具体步骤**：
1. 选钩子事件：
   - `pre_tool`：每次工具调用前（可阻断，返回非0阻止执行）
   - `post_tool`：每次工具调用后
   - `on_session_start`：新会话开始时
   - `on_session_end`：会话结束时
   - `on_agent_start`：agent 开始处理消息
   - `on_agent_end`：agent 处理完成
2. 填脚本绝对路径（脚本必须 `chmod +x` 可执行）
3. 脚本失败不会崩溃 agent（非阻塞，只记录错误）
4. 可配多个 hook，不同事件挂不同脚本

**验证**：`hermes config | grep hooks`，然后触发对应事件看脚本是否执行

---

### 16. Nous Tool Gateway（付费订阅专属）

**不配**：需要分别注册 Firecrawl/FAL/ElevenLabs/Browserbase 四个服务的 API key 才能用搜索/图片/TTS/浏览器功能，管理 4 套账单。

**配了**：付费 Nous Portal 订阅用户免额外 key 直接用这 4 项工具，全走订阅账单，一个 key 管四件套。

**具体步骤**：
1. 前置：需付费 Nous Portal 订阅（https://portal.nousresearch.com/manage-subscription）
2. 选要启用的工具：
   - `web`：Web 搜索+提取（替代 TAVILY_API_KEY / FIRECRAWL_API_KEY）
   - `image`：图片生成（替代 FAL_KEY，8 模型含 FLUX/GPT-Image）
   - `tts`：文本转语音（替代 VOICE_TOOLS_OPENAI_KEY / ELEVENLABS_API_KEY）
   - `browser`：浏览器自动化（替代 BROWSER_USE_API_KEY / BROWSERBASE_API_KEY）
3. 每个工具设 `enabled=true`
4. 不需要单独注册任何 API key

**验证**：`hermes status | grep 'Tool Gateway'`，确认激活状态

---

## 代码审查已修复的坑（v4.0 审查记录）

| 坑 | 症状 | 修复 |
|---|------|------|
| 批量配 auxiliary 不设 api_key_env | 密钥写了 .env 但 Hermes 不读 | 循环里必须 `hermes config set auxiliary.{task}.api_key_env ENV_VAR` |
| Tavily 不设 tavily_api_key_env | 同上 | `hermes config set web.tavily_api_key_env TAVILY_API_KEY` |
| provider_routing.only 逐个 set 覆盖 | 白名单只留最后一个 | 逗号拼接一次写入 `Anthropic,Google` |
| "inactive" 包含 "active" | 订阅检测误判 | 用 `.split()` 精确词匹配，不要 `"active" in status` |
| custom provider 空 base_url | 请求必挂 | 空 base_url 直接 return 退出 |
| hermes dashboard 前台跑 | 30s 超时被杀 | 必须 `background=True` |
| context.engine 选 compressor 不写入 | 旧引擎残留 | 无论选什么都要显式 set |

## 代码审查典型问题清单

| 类别 | 问题 | 修复模式 |
|------|------|----------|
| env 路径断裂 | 写 .env 但没 `hermes config set xxx.api_key_env` | 写 env 后必须配对应 config 路径 |
| 空值回退 | 用户跳过必填项仍写入配置 | 空 key → 回退兜底方案 or return |
| 逐项 set 覆盖 | 循环 `config set key=val` 覆盖前值 | 列表/逗号拼接一次写入 |
| 长运行阻塞 | dashboard/gateway 前台跑超时被杀 | 必须 `background=True` |
| 字符串子串误判 | `"active" in "inactive"` 为 True | 改 `.split()` 精确词匹配 |
| 校验缺失 | 策略/事件名/选项任意输入直接写入 | 白名单校验 + 无效回退默认值 |
| 创建失败不检测 | `run()` 返回布尔未检查 | `if not run(cmd): return` |
| 只提示不执行 | cron 等 feat 只 print 命令不执行 | 先问是否执行，否再 print 提示 |
| 文件路径不验证 | hook 脚本路径不检查存在性 | `os.path.isfile()` + 确认继续 |

## 安全规则（写脚本必须遵守）

1. **`shell=True` + 用户输入拼接 = 命令注入** — 必须用列表传参：`subprocess.run(["hermes", "config", "set", key, value])`
2. **API Key 绝对不能明文写 config.yaml** — 必须写 `.env`，Hermes 自动从环境变量读取
3. **`.env` 必须设 0600 权限** — `os.chmod(ENV_PATH, stat.S_IRUSR | stat.S_IWUSR)`
4. **`.env` 写入要去重** — 已有 key 精确替换，不能盲追加
5. **后台进程不能用 shell 的 `&`** — 用 `Popen(cmd, start_new_session=True)`
6. **用户输入拼入示例命令必须转义** — `shlex.quote()`

## patch 工具缩进坑

patch 工具对 Python 缩进极脆弱。超过 5 行的缩进敏感替换，用 `python3` 脚本精确修改。

## 角色审查流程

写完脚本后，必须调用 agency-agents-zh 角色库复核：
1. **代码审查员** — 按 🔴阻塞/🟡建议/💭小改进 分级
2. **安全工程师** — 对抗性思维检查
3. **Karpathy 编码元规则** — 最终走查

复核轮数：小脚本 1 次，中等 2 次，大项目分段。核到零阻塞项为止。

## 验证总清单

```bash
hermes config                    # 查看当前配置
hermes config | grep auxiliary   # 副驾模型
hermes config | grep web         # 搜索后端
hermes config | grep memory      # 记忆系统
hermes auth list                 # 密钥池
hermes profile list              # 分身
hermes cron list                 # 定时任务
hermes skills list               # 已装 skill
hermes config | grep compression # 压缩配置
hermes config | grep fallback    # 容灾配置
hermes config | grep hooks       # 钩子配置
hermes status | grep Gateway     # Tool Gateway 状态
```

⚠️ 修改配置后需重启网关才能生效：`/restart`
