# 开源本地部署个人效率工具调研

> 基于约束条件筛选：Air-gapped 内网 | Windows + 统信 UOS | Python 为主 | 无 USB | 企业微信 | 内网 OpenAI 兼容 AI

---

## 一、网页自动化采集（P0）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 1 | **Playwright** | microsoft/playwright | Microsoft 出品，跨平台网页自动化框架，支持 Chromium/Firefox/WebKit，Python/Node/Java/.NET 多语言 | 87k+ stars，行业标准，代码生成器 + Trace Viewer 强大，但浏览器二进制需首次下载 | ⭐⭐⭐⭐⭐ 核心框架，必须 |
| 2 | **Crawl4AI** | unclecode/crawl4ai | Python 原生 LLM 友好网页爬虫，异步架构，内置反 bot 检测，输出 LLM-ready Markdown | #1 趋势 GitHub 仓库，v0.8.6 修复 PyPI 供应链攻击，3 层反 bot 自动检测，无需 LLM 也可提取 JSON | ⭐⭐⭐⭐ 纯 Python，需 Playwright 浏览器 |
| 3 | **Firecrawl** | firecrawl/firecrawl | 全功能网页抓取平台，LLM 结构化提取，支持搜索/抓取/交互，Python/Node/Go/Rust SDK | 70k+ stars，开源版可自托管，Cloud 版需 API key，自托管需 Docker + GPU | ⭐⭐⭐ 自托管可行，但资源消耗大 |
| 4 | **Scrapy** | scrapy/scrapy | Python 老牌爬虫框架，异步 + 中间件架构，适合大规模爬取 | 60k+ stars，生态成熟但学习曲线陡，不适合 JS 渲染页面，需配合 Splash/Playwright | ⭐⭐⭐⭐ 纯 Python，内网友好 |
| 5 | **tbelorg/RPA-Python** | tebelorg/RPA-Python | Python RPA 库，桌面 + 网页自动化，支持图像识别 + 坐标点击 | 10k+ stars，简单直接，但文档较少，跨平台支持一般 | ⭐⭐⭐ 适合简单桌面操作 |
| 6 | **Robot Framework** | robotframework/robotframework | 通用自动化框架，关键字驱动，支持 Web/桌面/API 自动化，Python 生态 | 20k+ stars，企业级 RPA 标准，学习曲线中等，社区插件丰富 | ⭐⭐⭐⭐ 跨平台优秀 |
| 7 | **openrpa** | open-rpa/openrpa | 开源企业级 RPA 平台，可视化流程设计，Windows 为主 | 5k+ stars，功能强大但 Linux 支持弱，适合 Windows 办公场景 | ⭐⭐ Linux 支持不足 |
| 8 | **rpaframework** | RoboticCode/rpaframework | RPA 专用 Python 库集合，含浏览器/桌面/邮件/文件操作 | Robot Framework 官方库，维护活跃，文档完善 | ⭐⭐⭐⭐ Python 原生 |
| 9 | **Doppelgänger** | (Reddit r/selfhosted) | 基于 Playwright 的自托管网页自动化，可视化工作流 | Reddit 热议项目，免费无 per-run 成本，数据不出本地，但项目较新 | ⭐⭐⭐⭐ 需进一步验证 |
| 10 | **Spider** | spider-cloud/spider | 开源网页抓取平台，对标 Firecrawl，支持结构化提取 | 新兴项目，基准测试显示吞吐量优于 Crawl4AI，但社区较小 | ⭐⭐⭐ 需验证内网部署 |

---

## 二、文档解析与知识库（P0）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 11 | **MinerU** | opendatalab/MinerU | 商汤开源文档解析工具，PDF/Word/PPT/XLSX 高精度解析，图文表格保留 | 中文 PDF 优化最佳，v3.1 支持多 GPU 部署，mineru-router 负载均衡，CLI/API 双模式 | ⭐⭐⭐⭐⭐ 中文场景首选 |
| 12 | **Docling** | docling-project/docling | IBM 出品文档处理工具包，PDF 布局分析 + 表格识别，输出 Markdown/HTML/JSON | MIT 许可，LF AI & Data 托管，Heron 布局模型快速，表格识别强于 MinerU，但中文 OCR 弱 | ⭐⭐⭐⭐ 英文文档强 |
| 13 | **SiYuan (思源笔记)** | siyuan-note/siyuan | 隐私优先自托管知识库，本地 Markdown 存储，PDF 批注，跨平台，API 完整 | 43.9k stars，中文社区活跃，B3log 生态完善，插件系统 Petal API，移动端全平台 | ⭐⭐⭐⭐⭐ 核心知识库 |
| 14 | **Joplin** | laurent22/joplin | 开源笔记应用，端到端加密，多端同步，插件生态 | 38k+ stars，AGPL 许可，同步需自建（Nextcloud/WebDAV），无内置 AI | ⭐⭐⭐⭐ 备选知识库 |
| 15 | **Paperless-ngx** | paperless-ngx/paperless-ngx | 自托管文档管理系统，OCR + 标签 + 全文搜索，Docker 一键部署 | 28k+ stars，Tesseract OCR 较弱，可集成 EasyOCR/docTR，适合归档管理 | ⭐⭐⭐ 适合文档归档 |
| 16 | **Trilium Notes** | zadam/trilium | 层级笔记应用，自托管，支持脚本 + 同步 + 加密 | 18k+ stars，功能强大但 UI 较老，适合技术用户 | ⭐⭐⭐⭐ |
| 17 | **Obsidian (非开源但本地)** | - | 本地 Markdown 笔记，插件生态丰富，需手动同步 | 非开源，但数据完全本地，Obsidian 插件可本地运行 | ⭐⭐⭐⭐ 非开源但可用 |
| 18 | **Docuglean** | (GitHub Discussion) | 社区项目，OCR + PDF 解析，替代 Tesseract | 社区讨论项目，非正式维护，适合实验 | ⭐⭐ 不推荐生产 |

---

## 三、本地 AI 推理（P0）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 19 | **Ollama** | ollama/ollama | 最流行的本地 LLM 运行工具，OpenAI 兼容 API，模型管理简单 | 85k+ stars，一行命令运行，模型库丰富（Llama/Mistral/Qwen/DeepSeek），工具调用支持 | ⭐⭐⭐⭐⭐ 首选推理服务器 |
| 20 | **vLLM** | vllm-project/vllm | 高吞吐 LLM 推理服务器，PagedAttention，OpenAI 兼容 API | 35k+ stars，吞吐量远超 Ollama，适合多并发，但配置复杂需 GPU | ⭐⭐⭐⭐ 高并发场景 |
| 21 | **LocalAI** | mudler/localAI | 自托管 AI 引擎，支持 36+ 后端（llama.cpp/vLLM/transformers），OpenAI 兼容 | 15k+ stars，万能兼容层，可替换任何 OpenAI 调用，但性能不如原生 | ⭐⭐⭐⭐ 兼容层首选 |
| 22 | **llama.cpp** | ggerganov/llama.cpp | GGUF 格式本地推理，CPU/GPU 混合，极低资源消耗 | 85k+ stars，量化模型生态最丰富，CPU 也能跑 7B 模型，但速度慢 | ⭐⭐⭐⭐⭐ 低算力首选 |
| 23 | **Jan** | janhq/jan | 本地 LLM 桌面应用，OpenAI 兼容 API，跨平台 | 10k+ stars，UI 友好，类似 Ollama 但带 GUI，适合非技术用户 | ⭐⭐⭐⭐ |
| 24 | **LM Studio** | lmstudio/lmstudio | 本地 LLM 桌面应用，模型市场 + 推理 + API | 非开源，但可本地运行，UI 最友好，适合快速测试 | ⭐⭐⭐ 非开源 |
| 25 | **text-generation-webui** | oobabooga/text-generation-webui | 本地 LLM Web UI，支持 20+ 后端，插件生态 | 30k+ stars，功能最全但配置复杂，适合高级用户 | ⭐⭐⭐ |

---

## 四、RAG 与知识检索（P0）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 26 | **LangChain** | langchain-ai/langchain | LLM 应用开发框架，RAG/Agent/Chain，Python/JS | 95k+ stars，生态最大但被批评过于复杂，简单 RAG 可用 vanilla Python | ⭐⭐⭐⭐⭐ 框架首选 |
| 27 | **LlamaIndex** | run-llama/llama_index | 文档 Agent 框架，专注 RAG 和数据连接，Python/TS | 35k+ stars，RAG 场景比 LangChain 更简洁，文档解析集成好 | ⭐⭐⭐⭐⭐ RAG 首选 |
| 28 | **Khoj** | khoj-ai/khoj | 本地 AI 知识库，支持 Obsidian/SiYuan/Markdown，RAG + 搜索 | 10k+ stars，自托管简单，可连接本地 LLM，但配置需调优 | ⭐⭐⭐⭐ |
| 29 | **PrivateGPT** | zylon-ai/private-gpt | 100% 本地 RAG，文档问答，无需 API key | 25k+ stars，开箱即用但性能一般，适合快速验证 | ⭐⭐⭐ |
| 30 | **GPT4All** | nomic-ai/gpt4all | 本地 LLM 生态系统，含推理 + RAG + 桌面应用 | 30k+ stars，Nomic 出品，模型优化好，但 RAG 功能较弱 | ⭐⭐⭐ |

---

## 五、任务调度与容错（P1）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 31 | **Tenacity** | jd/tenacity | Python 重试库，装饰器语法，指数退避，灵活配置 | Apache 2.0，轻量无依赖，一行代码加重试，社区稳定 | ⭐⭐⭐⭐⭐ 容错核心 |
| 32 | **APScheduler** |apscheduler/apscheduler | Python 任务调度库，支持 cron/interval/date 触发，持久化 | 8k+ stars，比 cron 灵活，支持数据库持久化，跨平台 | ⭐⭐⭐⭐⭐ 调度核心 |
| 33 | **Dkron** | distribworks/dkron | 分布式 Cron 服务，故障容忍，Web UI | 5k+ stars，适合多节点，单节点用 APScheduler 更简单 | ⭐⭐⭐ 多节点场景 |
| 34 | **Celery** | celery/celery | 分布式任务队列，Redis/RabbitMQ 后端，支持重试 | 25k+ stars，功能强大但依赖 Redis，内网需自建 Redis | ⭐⭐⭐ 需 Redis |
| 35 | **RQ (Redis Queue)** | rq/rq | 简单 Python 任务队列，Redis 后端 | 14k+ stars，比 Celery 简单，但仍需 Redis | ⭐⭐⭐ 需 Redis |
| 36 | **Hermes Cron** | (本地) | 当前使用的内置定时任务系统，支持 deliver 到飞书 | 已验证可用，6 个自审任务稳定运行 | ⭐⭐⭐⭐⭐ 已部署 |

---

## 六、企业微信集成（P1）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 37 | **wecom-bot-mcp-server** | loonghao/wecom-bot-mcp-server | 企业微信 Bot MCP 服务器，标准接口供 AI 调用 | 新兴项目，MCP 协议标准化，适合 AI Agent 集成 | ⭐⭐⭐⭐⭐ 首选 |
| 38 | **go-wecom-bot** | futuretea/go-wecom-bot | 企业微信 Bot Go SDK，Webhook 消息推送 | 轻量 SDK，Go 语言，Python 需找其他 | ⭐⭐⭐ Go 语言 |
| 39 | **wecom-bot-api** | go-sphere/wecom-bot-api | 完整企业微信 Bot SDK，回调 + 加密 + 模板卡片 | Go 语言，功能全面 | ⭐⭐⭐ Go 语言 |
| 40 | **WeCom 自建应用 Webhook** | 企业微信官方 | 企业微信官方机器人 Webhook，无需 SDK | 官方支持，最简单，文本/Markdown/图片/卡片 | ⭐⭐⭐⭐⭐ 最简单 |

---

## 七、工作流自动化（P2）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 41 | **n8n** | n8n-io/n8n | 工作流自动化平台，400+ 集成，fair-code 许可，自托管 | 187k stars，功能最强，Python/JS 代码节点，Git 版本控制，AI Agent 支持 | ⭐⭐⭐⭐⭐ Docker 部署 |
| 42 | **n8n Self-Hosted AI Starter Kit** | n8n-io/self-hosted-ai-starter-kit | n8n + Ollama + Flowise 一键 Docker 部署 | 官方出品，开箱即用，适合快速搭建本地 AI 工作流 | ⭐⭐⭐⭐⭐ 推荐 |
| 43 | **AppFlowy** | AppFlowy-IO/AppFlowy | 开源 Notion 替代，本地优先，Flutter + Rust | 35k+ stars，UI 现代，但自动化功能弱 | ⭐⭐⭐ 笔记替代 |
| 44 | **Baserow** | baserow/baserow | 开源 Airtable 替代，数据库 + 自动化 | 20k+ stars，适合结构化数据管理 | ⭐⭐⭐ |
| 45 | **Vikunja** | go-vikunja/vikunja | 自托管任务管理，Kanban + 列表 + 日历 | 10k+ stars，轻量简洁，API 完整 | ⭐⭐⭐ |

---

## 八、其他效率工具（P2）

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 46 | **Super Productivity** | johannesjo/super-productivity | 任务 + 时间追踪 + 时间块，跨平台，GitHub/GitLab 集成 | 15k+ stars，离线优先，本地存储，无后端依赖 | ⭐⭐⭐⭐⭐ 完全离线 |
| 47 | **Taskwarrior** | GothenburgBitFactory/taskwarrior | 命令行任务管理，极简，本地存储 | 5k+ stars，CLI 友好，适合键盘流用户 | ⭐⭐⭐⭐⭐ 完全离线 |
| 48 | **Jellyfin** | jellyfin/jellyfin | 自托管媒体服务器，视频/音乐/图片管理 | 30k+ stars，适合个人媒体库管理 | ⭐⭐⭐ 非核心 |
| 49 | **Home Assistant** | home-assistant/core | 智能家居自动化，本地优先，2000+ 集成 | 80k+ stars，内网自动化强大，但需硬件支持 | ⭐⭐⭐ 场景受限 |
| 50 | **Awesome Self-Hosted** | awesome-selfhosted/awesome-selfhosted | 自托管项目大全，7000+ 项目分类索引 | 90k+ stars，不是工具而是目录，用于发现更多项目 | ⭐⭐⭐⭐⭐ 参考目录 |

---

## 九、内网约束适配总结

### ✅ 完全适配（无需外网依赖）
| 项目 | 说明 |
|------|------|
| Playwright | 首次需下载浏览器二进制，之后完全离线 |
| Crawl4AI | 依赖 Playwright，同上方 |
| MinerU | Python 包，首次 pip install 需外网，之后离线 |
| Docling | 同 MinerU |
| SiYuan | 下载安装包后完全离线 |
| Ollama | 首次拉取模型需外网，之后完全离线 |
| llama.cpp | 纯本地编译/运行 |
| LangChain/LlamaIndex | Python 包，首次 pip install 需外网 |
| Tenacity/APScheduler | 纯 Python，无外部依赖 |
| n8n | Docker 镜像需首次拉取，之后离线 |

### ⚠️ 需外网初始化
| 项目 | 外网依赖 | 解决方案 |
|------|---------|---------|
| Playwright 浏览器 | 首次下载 Chromium/Firefox | 外网设备下载后内网传输 |
| Ollama 模型 | 首次 pull 模型文件 | 外网 pull 后内网传输 |
| Python 包 (pip) | 首次 pip install | 外网下载 wheel 后内网安装 |
| Docker 镜像 | 首次 docker pull | 外网 pull 后 docker save 传输 |

### ❌ 不推荐（强依赖外网/云服务）
| 项目 | 原因 |
|------|------|
| Firecrawl Cloud | 需 API key + Cloud 服务 |
| Spider Cloud | 需 Cloud 服务 |
| LM Studio | 非开源，模型市场需外网 |
| Obsidian Sync | 需官方同步服务（可替代为本地同步） |

---

## 十、推荐技术栈组合

```
┌─────────────────────────────────────────────────────────┐
│              推荐内网效率工具技术栈                      │
├─────────────────────────────────────────────────────────┤
│  采集层    → Playwright + Crawl4AI (Python)             │
│  解析层    → MinerU (中文 PDF) / Docling (英文表格)      │
│  知识库    → SiYuan (本地 Markdown + PDF 批注)           │
│  AI 推理   → Ollama (首选) / llama.cpp (低算力)          │
│  RAG       → LlamaIndex (RAG 专用) / LangChain (通用)    │
│  调度容错  → APScheduler + Tenacity                      │
│  工作流    → n8n Self-Hosted (Docker)                    │
│  分发      → 企业微信 Webhook Bot                        │
│  文档解析  → MinerU → SiYuan → LlamaIndex RAG           │
└─────────────────────────────────────────────────────────┘
```

---

## 十一、测评来源

- GitHub 官方 README 及 Issues
- Reddit r/selfhosted / r/LocalLLaMA 社区讨论
- Hacker News 技术讨论
- 技术博客：Firecrawl Blog, Bright Data, Medium, Towards Data Science
- 基准测试：Spider vs Firecrawl vs Crawl4AI (1000 URLs 基准)
- 官方文档：Playwright, Ollama, MinerU, Docling, n8n

---

> 文档版本：v1.0 | 爬取时间：2026-05-15 | 项目总数：50 | 后续可增量更新
