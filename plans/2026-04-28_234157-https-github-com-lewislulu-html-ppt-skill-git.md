# 计划：安装PPT Skills → 调用角色写调研报告 → Hermes+Claude各生成PPT

## 目标

1. 安装两个PPT skill（html-ppt-skill、guizang-ppt-skill）
2. 将Hermes的skills共享给Claude Code，避免重复安装
3. 调用角色skills撰写Hermes Agent调研报告
4. 基于报告，Hermes用html-ppt-skill生成PPT，Claude Code用guizang-ppt-skill生成PPT

## 报告内容大纲（PPT素材来源）

### 一、历史
- Nous Research背景（去中心化AI研究实验室）
- 2026年2月25日发布v0.1.0
- 版本演进：v0.1→v0.5(3.28)→v0.9→v0.10(4.16,Tool Gateway)→v0.11(当前)
- 两个月GitHub 47K+ stars，1,556+ commits
- 定位：OpenClaw的安全替代品（OpenClaw 5700 skills中1467恶意）

### 二、现状
- v0.11.0，MIT开源
- 核心能力：Skills系统、持久记忆、定时任务、子代理委派、多平台网关
- 平台：Telegram/Discord/Slack/WhatsApp/Signal/Email/CLI/飞书/微信
- 五种后端：local/Docker/SSH/Singularity/Modal
- 100+内置skills，MCP协议支持，Atropos RL训练框架
- Web UI仪表盘（v0.11新增）

### 三、能做什么
- 编码助手（CLI/VPS上跑代码、review、debug）
- 多平台消息助手（跨平台对话、文件投递）
- 自动化调度（cron定时任务、巡检、备份）
- 研究助手（web搜索、论文抓取、信息整合）
- 创意生产（PPT、视频脚本、音乐、ASCII艺术）
- 数据科学（Jupyter内核、可视化）
- 智能家居/服务器运维

### 四、现有项目
- Hermes Agent本体：github.com/NousResearch/hermes-agent
- 官方文档站：hermes-agent.nousresearch.com
- Skills生态：agentskills.io规范、ClawHub迁移
- 社区：Discord、Reddit r/SideProject生态

### 五、存在的问题
- 模型兼容性：部分模型对结构化工具调用不稳定（如cronjob/hindsight）
- Skills质量参差：第三方skill无安全审计，恶意skill风险虽低于OpenClaw但仍存在
- 资源开销：长期运行的记忆/技能库膨胀，token消耗需优化
- 多代理协调：subagent深度有限（max_spawn_depth=2），复杂编排受限
- 文档滞后：快速迭代中部分文档与实际版本脱节
- Gateway稳定性：config结构异常导致投递失败等边界case

### 六、AI发展趋势
- Agent从工具调用→自主规划→自我改进（Hermes的skill自生成是雏形）
- 记忆系统从临时上下文→持久知识图谱→跨代理知识共享
- 安全从信任所有skills→沙箱隔离→形式化验证
- 多代理从单代理→有限委派→对等协作网络
- 本地化与隐私：VPS部署→端侧推理→联邦学习

---

## 执行步骤

### 阶段1：安装Skills + 共享配置

| 步骤 | 操作 | 负责方 |
|------|------|--------|
| 1.1 | `npx skills add https://github.com/lewislulu/html-ppt-skill` | Hermes终端 |
| 1.2 | `npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill` | Hermes终端 |
| 1.3 | 验证两个skill安装成功（`skills_list`查看） | Hermes |
| 1.4 | 将`~/.hermes/skills/`目录软链接或配置Claude Code的skill路径，使Claude Code可读取Hermes全部skills | Hermes终端 |

**1.4的具体方案**：Claude Code通过`CLAUDE.md`或`--skill-dir`参数指向`~/.hermes/skills/`，避免在Claude Code的工作目录重复clone。做法：
- 在Claude Code的项目目录创建`~/.claude/skills` → `~/.hermes/skills`的符号链接
- 或在CC的配置中指定skill搜索路径

### 阶段2：调用角色Skills写调研报告

| 步骤 | 操作 | 负责方 |
|------|------|--------|
| 2.1 | 调用角色skill撰写「Hermes Agent调研报告」，涵盖上述6大板块 | Hermes |
| 2.2 | 报告保存为`~/hermes-ppt-project/hermes-agent-report.md` | Hermes |
| 2.3 | 审核报告质量，确保6个板块内容完整、数据准确 | Hermes |

**角色选择**：从`~/agency-agents-zh/`调用「行业分析师」或「技术分析师」角色，加载其prompt到子代理上下文中，让其以专业分析师视角撰写报告。

### 阶段3：生成PPT（共4份）

| 步骤 | 操作 | 负责方 | Skill | 风格定位 |
|------|------|--------|-------|---------|
| 3.1 | 用html-ppt-skill生成PPT | Hermes | html-ppt-skill | 技术硬核风（hermes-cyber-terminal主题），突出架构/能力/技术细节 |
| 3.2 | 用guizang-ppt-skill生成PPT | Hermes | guizang-ppt-skill | 杂志人文风（电子墨水+WebGL），突出历史脉络/问题反思/趋势展望 |
| 3.3 | 用html-ppt-skill生成PPT | Claude Code | html-ppt-skill | 商业报告风（pitch-deck-vc主题），突出现状/项目/商业价值 |
| 3.4 | 用guizang-ppt-skill生成PPT | Claude Code | guizang-ppt-skill | 深度阅读风（衬线+大字报），突出问题/趋势/思辨 |
| 3.5 | 4份PPT保存到`~/hermes-ppt-project/`下不同子目录 | 各自 | - | - |
| 3.6 | 用户对比4份PPT效果 | 用户 | - | - |

**风格与报告内容的对应逻辑**：

- **html-ppt × Hermes**：hermes-cyber-terminal主题（暗色终端风）→ 适合展示Hermes的技术架构、工具链、五后端部署、skill系统等技术密集内容
- **guizang-ppt × Hermes**：杂志人文风 → 适合讲述Hermes的诞生故事（从OpenClaw安全危机到独立崛起）、存在的问题（模型兼容性/skill安全/token膨胀）、发展趋势的思辨
- **html-ppt × Claude Code**：pitch-deck-vc主题（商业路演风）→ 适合展示Hermes的市场定位、现有项目生态、社区规模(47K stars)、与竞品对比
- **guizang-ppt × Claude Code**：深度阅读风（大字报+数据可视化）→ 适合深度分析问题板块和趋势板块，用视觉冲击传达"AI Agent往哪走"

**输出路径**：
- `~/hermes-ppt-project/hermes-html-ppt/index.html`
- `~/hermes-ppt-project/hermes-guizang-ppt/index.html`
- `~/hermes-ppt-project/claude-html-ppt/index.html`
- `~/hermes-ppt-project/claude-guizang-ppt/index.html`

---

## 文件变更清单

| 路径 | 操作 |
|------|------|
| `~/.hermes/skills/creative/html-ppt/` | 新增（npx安装） |
| `~/.hermes/skills/creative/guizang-ppt-skill/` | 新增（npx安装） |
| `~/.claude/skills` → `~/.hermes/skills` | 新增符号链接 |
| `~/hermes-ppt-project/hermes-agent-report.md` | 新增（调研报告） |
| `~/hermes-ppt-project/html-ppt/index.html` | 新增（Hermes生成） |
| `~/hermes-ppt-project/html-ppt/images/` | 新增（图片目录） |
| `~/hermes-ppt-project/guizang-ppt/index.html` | 新增（Claude Code生成） |
| `~/hermes-ppt-project/guizang-ppt/images/` | 新增（图片目录） |

## 验证

- [ ] `skills_list`中可见html-ppt和guizang-ppt-skill
- [ ] `ls -la ~/.claude/skills`指向`~/.hermes/skills`
- [ ] 报告6个板块内容完整，无空壳段落
- [ ] 两个HTML PPT浏览器打开可正常翻页、动效生效
- [ ] PPT内容与报告一致，无遗漏板块

## 风险与开放问题

1. **npx skills add** 命令依赖Node.js环境和npm registry可达性，VPS网络受限时可能需要代理
2. **guizang-ppt-skill** 的template.html依赖CDN字体/JS，离线环境不可用
3. **Claude Code共享skills**：CC是否能直接读取Hermes skill格式取决于CC版本，需实测
4. **角色skill调用**：agency-agents-zh角色是中文prompt，子代理需支持中文推理
5. **报告数据时效**：Hermes快速迭代，发布时间线数据以GitHub releases页面为准，需二次核实
6. **WebGL兼容性**：guizang-ppt的shader在部分浏览器/设备可能不渲染，需备选方案
