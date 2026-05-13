---
name: web-scraping-toolkit
description: 爬取工具选型与升级决策框架 — 根据场景选择最优爬取工具，评估资源开销和安全风险。当需要提升爬取能力、选择爬虫工具、评估反爬方案、或对比crawl4ai vs scrapling时加载。
version: "1.0"
---

# Web Scraping Toolkit 选型框架

## 当前已装工具

| 工具 | 能力 | 适用场景 |
|---|---|---|
| **Scrapling** | HTTP/Dynamic/Stealth三模式，Cloudflare绕过，Spider框架 | 单页抓取、反爬绕过、结构化爬虫 |
| **Crawl4AI** | 异步批量爬取，AI友好markdown输出，6x速度 | 整站爬取、批量采集、AI数据管道 |
| **web_extract** | 简单URL提取转markdown | 轻量页面、无反爬 |
| **wechat-article-fetch** | requests+Android UA绕微信验证码 | 微信公众号文章 |

## 工具选型决策树

```
目标页面有反爬（Cloudflare等）？
├─ 是 → Scrapling stealthy-fetch 失败？
│   └─ 是 → Crawl4AI Undetected模式 (headless=False + UndetectedAdapter + magic)
└─ 否 → 需要批量爬取整站？
 ├─ 是 → Crawl4AI arun_many + Dispatcher
 └─ 否 → 需要Markdown/结构化提取/LLM提取？
     ├─ 是 → Crawl4AI (核心优势)
     └─ 否 → 单页提取？
         ├─ 简单页面 → web_extract
         ├─ 微信文章 → wechat-article-fetch
         └─ JS渲染页面 → Scrapling fetch / Crawl4AI普通模式
```

**渐进式升级**: web_extract → Scrapling get → Scrapling fetch → Scrapling stealthy-fetch → Crawl4AI stealth → Crawl4AI Undetected

## Crawl4AI vs Scrapling 互补关系

| 维度 | Crawl4AI | Scrapling |
|------|----------|-----------|
| 核心优势 | Markdown输出、LLM提取、深度爬取 | 自愈选择器、轻量反检测 |
| 反检测 | stealth + Undetected(patchright) | Camoufox + PlaywrightStealth |
| 结构化提取 | CSS/XPath/LLM/Regex/Cosine | CSS + 自适应选择器 |
| Spider | BFS/DFS/BestFirst/Adaptive | Scrapy-like + 暂停恢复 |
| 自愈选择器 | ❌ | ✅ |
| LLM集成 | ✅ 原生 | ❌ |
| Docker | ✅ 官方镜像 | ❌ |
| Hook定制 | ✅ 8个钩子点 | ❌ |

**互补组合**: Scrapling做反检测+自适应定位 → Crawl4AI做Markdown生成+LLM提取

## 已评估但未安装的工具

### Jina Reader
- **用法**: URL前加 `r.jina.ai/`
- **优点**: 零部署，免费额度大，支持PDF/图片
- **缺点**: 延迟高，依赖云服务
- **适用**: web_extract失败时的快速备用方案

### Firecrawl
- **优点**: 功能最全（scrape/crawl/search/extract/agent）
- **自建要求**: 实际4GB+ RAM稳跑，Docker部署
- **云服务**: 付费
- **结论**: 本机3.8GB RAM装了会OOM，8GB+机器才考虑

### Parallel CLI (inference.sh)
- **本质**: 云端AI应用市场CLI，不是爬虫工具
- **结论**: 对爬取能力无实质提升，不装

### ScrapeGraphAI / puppeteer-extra-stealth / Stagehand
- 均已评估，现有工具链已覆盖同等能力，不装

## 本机资源现状（2026-04）

- CPU: 4核 / RAM: 3.8GB + 2GB swap / 磁盘: 18GB空闲
- Playwright+Chromium缓存1.3GB（Scrapling/Crawl4AI共用）
- 关键依赖已装: playwright, beautifulsoup4, lxml, aiofiles

## 文档站抓取专用流程

当目标是从文档站（Docusaurus/MkDocs/GitBook）抓取内容入 Wiki 时，**不走上面的通用爬取流程**，用专用脚本：

```bash
# 推荐：直接从 GitHub 源仓库拉原始 markdown（最快、最完整）
python3 ~/.hermes/scripts/wiki_ingest.py <站点URL> \
  --github <owner/repo> --docs-path <docs目录>

# 只抓子目录
python3 ~/.hermes/scripts/wiki_ingest.py <URL> \
  --github <owner/repo> --docs-path <路径> --filter reference

# dry run 先看会抓什么
python3 ~/.hermes/scripts/wiki_ingest.py <URL> \
  --github <owner/repo> --docs-path <路径> --dry-run
```

**为什么不用 web_extract/浏览器？**
- web_extract 对文档站截断在~5KB，大量内容丢失
- 浏览器 JS 提取能拿完整内容但极慢
- GitHub raw curl 最快且拿完整原文，Docusaurus/MkDocs 源码必在 GitHub

**策略优先级**: GitHub raw > curl直拉 > web_extract(fallback) > 浏览器JS(最后手段)

脚本自动完成：raw存储 → wiki页生成 → index/log更新 → lint校验 → git push

## 安全守则

1. 绝不在聊天中明文发送token/密钥 — 用环境变量注入
2. 敏感凭证只通过服务器终端直接操作，不经过AI对话
3. Crawl4AI和Scrapling均本地运行，不回传数据
4. 新工具安装前必须评估资源开销和供应链安全
