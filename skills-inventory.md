# Hermes Skills 清单

- 活跃: **80** 个（日常加载）
- 冷备: **43** 个（移至cold/目录，需手动恢复）
- 删除: **22** 个（VPS上永远用不到）

---

# 一、活跃 Skills

## automation — 自动化脚本 (1个)

- **tencentyun-seckill**: 腾讯云秒杀抢购脚本操作指南 — cookies/csrf-token配置、后台运行、性能优化

## autonomous-ai-agents — 自主AI代理 (4个)

- **claude-code**: Delegate coding tasks to Claude Code (Anthropic's CLI agent). Use for building features, refactoring, PR reviews, and it
- **codex**: Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fix
- **hermes-agent**: Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gatewa
- **opencode**: Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonom

## creative — 创意内容生成 (8个)

- **architecture-diagram**: Generate dark-themed SVG diagrams of software systems and cloud infrastructure as standalone HTML files with inline SVG 
- **ascii-art**: Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs (asciified, ascii.co.u
- **baoyu-comic**: Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed pane
- **baoyu-infographic**: Generate professional infographics with 21 layout types and 21 visual styles. Analyzes content, recommends layout×style 
- **creative-ideation**: Generate project ideas through creative constraints. Use when the user says 'I want to build something', 'give me a proj
- **excalidraw**: Create hand-drawn style diagrams using Excalidraw JSON format. Generate .excalidraw files for architecture diagrams, flo
- **popular-web-designs**: >
- **songwriting-and-ai-music**: >

## data-science — 数据科学 (1个)

- **jupyter-live-kernel**: >

## devops — 运维部署 (10个)

- **cc-switch-setup**: 在headless Linux VPS上部署CC Switch CLI + Claude Code的完整流程。包括安装、provider配置（非交互式）、proxy启动、环境变量、开机自启、验证。适用于无法使用GUI的场景。
- **daily-self-audit**: 每日自主审核与优化流程 — 分三层：自动执行（缓存/cron清理）、需确认（memory/skill变更）、砍掉做不到的。cron定时触发，报告+执行合一。
- **feishu-media-file-delivery**: 飞书文件附件发送的修补方案——Hermes send_message 工具层拦截了飞书 MEDIA 分发，需要改两处代码才能让飞书支持文件附件发送。
- **hermes-backup-sanitize-deploy**: Full backup of Hermes Agent + Hindsight + CC Switch + Claude Code to GitHub, sanitize all secrets, and create setup/set-
- **hermes-config-setup**: 交互式脚本引导用户配置 Hermes Agent 的副驾模型、搜索后端、记忆系统、进阶功能（Profile/Skill进化/并发/Cron/Token监控/生态工具），支持自定义厂商(base_url+api_key)，API Key 写 
- **hermes-token-optimization**: Interactive guide script for optimizing Hermes Agent token consumption via compression, auxiliary models, search backend
- **hindsight-troubleshooting**: Hindsight 本地嵌入模式排错指南 — 从模块缺失到 glibc 不兼容的完整诊断链路。
- **install-third-party-skills**: 从 GitHub 安装第三方 Hermes Agent skills 的标准流程。clone → 定位 SKILL.md → 拷贝到 skills 目录 → 清理临时文件。适用于 agent-browser、marketing-skills
- **vps-init-script**: Use when creating or optimizing VPS initialization scripts for Ubuntu/Debian servers — covers system setup, performance 
- **webhook-subscriptions**: Create and manage webhook subscriptions for event-driven agent activation, or for direct push notifications (zero LLM co

## dogfood — Web应用测试 (1个)

- **dogfood**: Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports

## github — GitHub工作流 (8个)

- **codebase-inspection**: Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. Use when a
- **github-auth**: Set up GitHub authentication for the agent using git (universally available) or the gh CLI. Covers HTTPS tokens, SSH key
- **github-code-review**: Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. Wor
- **github-issues**: Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Wor
- **github-pr-workflow**: Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge
- **github-repo-create-push**: 通过 SSH key 在 GitHub 创建新仓库并推送本地文件
- **github-repo-management**: Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works 
- **github-repo-push-scripts**: 将服务器上的脚本文件推送至GitHub仓库的完整流程——SSH key认证 + API创建仓库 + git push。

## knowledge — 知识库 (1个)

- **agency-agents-zh**: 中文 AI Agent 角色库 — 212 个专业角色提示词，覆盖 18 个部门。通过文件路径加载任意角色，快速切换专业视角。

## marketing — 营销 (6个)

- **content-strategy**: When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also 
- **copywriting**: When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, prici
- **marketing-ideas**: When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the us
- **seo-audit**: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit,"
- **social-content**: When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, Ti
- **video**: When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use wh

## mcp — MCP协议 (1个)

- **native-mcp**: Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers

## media — 媒体内容 (2个)

- **gif-search**: Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. Useful for finding reaction GIFs, cr
- **youtube-content**: >

## mlops — ML运维 (4个)

- **weights-and-biases**: Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and 
- **huggingface-hub**: Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, dep
- **segment-anything**: Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using
- **dspy**: Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and ag

## note-taking — 笔记 (1个)

- **obsidian**: Read, search, and create notes in the Obsidian vault.

## productivity — 生产力工具 (7个)

- **google-workspace**: Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the
- **linear**: Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key
- **maps**: >
- **nano-pdf**: Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make con
- **notion**: Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion wor
- **ocr-and-documents**: Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker
- **powerpoint**: Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide d

## research — 学术研究 (4个)

- **arxiv**: Search and retrieve academic papers from arXiv using their free REST API. No API key needed. Search by keyword, author, 
- **blogwatcher**: Monitor blogs and RSS/Atom feeds for updates using the blogwatcher-cli tool. Add blogs, scan for new articles, track rea
- **llm-wiki**: Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. Ingest sources, query compil
- **research-paper-writing**: End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and

## software-development — 软件开发 (10个)

- **karpathy-coding-guidelines**: Karpathy 编码元规则 — 4 条横切所有编码工作的铁律，优先级高于角色库。写代码前必须加载，防止过度工程、错误假设、无关修改和模糊目标。
- **plan**: Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, an
- **subagent-driven-development**: Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage r
- **superpowers-receiving-code-review**: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or techni
- **superpowers-requesting-code-review**: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- **superpowers-systematic-debugging**: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- **superpowers-test-driven-development**: Use when implementing any feature or bugfix, before writing implementation code
- **superpowers-verification-before-completion**: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verifi
- **superpowers-writing-plans**: Use when you have a spec or requirements for a multi-step task, before touching code
- **superpowers-writing-skills**: Use when creating new skills, editing existing skills, or verifying skills work before deployment

## tools — 工具集 (2个)

- **context7-skills**: Use when managing Context7 CLI skills with npx ctx7 (search, install, list, remove, info).
- **weather-query**: 天气查询脚本 v2 — 三源融合（tianqi24/Open-Meteo/wttr.in），15天预报+24小时逐时+空气质量

## video-prompting — 视频提示词 (1个)

- **video-prompting**: Draft and refine prompts for video generation models (text-to-video and image-to-video), and create character-sheet prom

## web — 网络爬取 (7个)

- **agent-browser**: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, fil
- **core**: Core agent-browser usage guide. Read this before running any agent-browser commands. Covers the snapshot-and-ref workflo
- **crawl4ai**: AI-native web crawler with JS rendering, stealth mode, structured extraction (CSS/XPath/LLM/Regex), Markdown generation,
- **scrapling**: Scrape web pages using Scrapling with anti-bot bypass (like Cloudflare Turnstile), stealth headless browsing, spiders fr
- **university-admission-docs**: 下载和整理高校招生简章（博士/硕士）的实操流程 — 从官网定位到多源抓取、文件整合的完整方法论。
- **web-scraping-toolkit**: 爬取工具选型与升级决策框架 — 根据场景选择最优爬取工具，评估资源开销和安全风险。当需要提升爬取能力、选择爬虫工具、评估反爬方案、或对比crawl4ai vs scrapling时加载。
- **wechat-article-fetch**: 抓取微信公众号文章内容的方法论，绕过验证码和防爬机制。

## workflow — 工作流 (1个)

- **interactive-cli-execution**: Workflow for executing and interacting with CLI scripts that prompt for continuous standard input.

---

# 二、冷备 Skills

移至 `~/.hermes/skills/cold/`，不日常加载。

**恢复方法：**

```bash
mv ~/.hermes/skills/cold/<分类>/<skill名> ~/.hermes/skills/<分类>/
```

## creative (4个)

- **ascii-video**: Production pipeline for ASCII art video — any format. Converts video/audio/images/generative input into colored ASCII ch
- **manim-video**: Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style e
- **p5js**: Production pipeline for interactive and generative visual art using p5.js. Creates browser-based sketches, generative ar
- **pixel-art**: Convert images into retro pixel art with hardware-accurate palettes (NES, Game Boy, PICO-8, C64, etc.), and animate them

## marketing (34个)

- **ab-test-setup**: When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. 
- **ad-creative**: When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad varia
- **ai-seo**: When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Als
- **analytics-tracking**: When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "se
- **aso-audit**: When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit
- **churn-prevention**: When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement
- **cold-email**: Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, p
- **community-marketing**: Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a com
- **competitor-alternatives**: When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the
- **competitor-profiling**: When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'compe
- **copy-editing**: When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the 
- **customer-research**: When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research,
- **directory-submissions**: When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlin
- **email-sequence**: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email pro
- **form-cro**: When the user wants to optimize any form that is NOT signup/registration — including lead capture forms, contact forms, 
- **free-tool-strategy**: When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or bran
- **image**: When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product 
- **launch-strategy**: When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions
- **lead-magnets**: When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the u
- **marketing-psychology**: When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when 
- **onboarding-cro**: When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also us
- **page-cro**: When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pa
- **paid-ads**: When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, 
- **paywall-upgrade-cro**: When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use wh
- **popup-cro**: When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also 
- **pricing-strategy**: When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'p
- **product-marketing-context**: When the user wants to create or update their product marketing context document. Also use when the user mentions 'produ
- **programmatic-seo**: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "progr
- **referral-program**: When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Al
- **revops**: When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Al
- **sales-enablement**: When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also 
- **schema-markup**: When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user men
- **signup-flow-cro**: When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the use
- **site-architecture**: When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal 

## media (2个)

- **heartmula**: Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + 
- **songsee**: Generate spectrograms and audio feature visualizations (mel, chroma, MFCC, tempogram, etc.) from audio files via CLI. Us

## red-teaming (1个)

- **godmode**: Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC sys

## research (1个)

- **polymarket**: Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. Read-only via publi

## social-media (1个)

- **xurl**: Interact with X/Twitter via xurl, the official X API CLI. Use for posting, replying, quoting, searching, timelines, ment

---

# 三、已删除 Skills

VPS上永远用不到：

## apple (4个)

- apple-notes
- apple-reminders
- findmy
- imessage

## email (1个)

- himalaya

## gaming (2个)

- minecraft-modpack-server
- pokemon-player

## mlops (10个)

- lm-evaluation-harness
- llama-cpp
- obliteratus
- outlines
- vllm
- audiocraft
- segment-anything-model
- axolotl
- trl-fine-tuning
- unsloth

## smart-home (1个)

- openhue

## software-development (4个)

- requesting-code-review
- systematic-debugging
- test-driven-development
- writing-plans

