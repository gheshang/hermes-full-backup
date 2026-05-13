---
name: crawl4ai
description: AI-native web crawler with JS rendering, stealth mode, structured extraction (CSS/XPath/LLM/Regex), Markdown generation, deep crawling (BFS/DFS/BestFirst), batch crawling, screenshots/PDF, and session management. Use when web_extract fails; need JS-rendered content; need structured data extraction; need Markdown output for LLM/RAG; batch crawling multiple URLs; deep crawling/spidering a site; Scrapling stealthy-fetch still gets blocked; or need LLM-powered semantic extraction.
version: "0.8.6"
metadata:
  hermes:
    tags: [crawl, scrape, js-render, stealth, llm-extraction, markdown, spider, batch, screenshot, pdf, anti-bot]
    related_skills: [scrapling, wechat-article-fetch]
---

# Crawl4AI

Crawl4AI is an AI-native web crawling framework — every output is optimized for LLM consumption (Markdown, structured JSON, fit content). Three anti-detection tiers, five extraction strategies, deep crawling with smart prioritization, and full JS interaction via sessions.

**Requires: Python 3.10+, crawl4ai 0.8.6+, patchright (for undetected mode)**

## Tool Selection Guide

| 场景 | 用什么 |
|------|--------|
| 简单HTTP抓取，无JS | `scrapling extract get` 或 `web_extract` |
| JS渲染页面 | `scrapling extract fetch` 或 Crawl4AI 普通模式 |
| 反爬/Cloudflare | `scrapling extract stealthy-fetch` |
| 反爬+需要更强stealth | Crawl4AI Undetected模式 |
| 需要Markdown输出 | Crawl4AI（核心优势） |
| 需要结构化提取(CSS/XPath) | Crawl4AI `JsonCssExtractionStrategy` / `JsonXPathExtractionStrategy` |
| 需要语义提取(LLM) | Crawl4AI `LLMExtractionStrategy` |
| 批量爬取多URL | Crawl4AI `arun_many` + Dispatcher |
| 深度爬取/整站Spider | Crawl4AI `BestFirstCrawlingStrategy` |
| 微信公众号 | `wechat-article-fetch` skill |
| 截图/PDF | Crawl4AI `screenshot=True` / `pdf=True` |

**渐进式升级**: web_extract → scrapling get → scrapling fetch → scrapling stealthy-fetch → Crawl4AI stealth → Crawl4AI undetected

---

## Core API

### BrowserConfig — 浏览器启动配置

```python
from crawl4ai import BrowserConfig

browser_cfg = BrowserConfig(
    headless=True,              # 生产用True，调试用False
    browser_type="chromium",    # "chromium" | "firefox" | "webkit"
    viewport_width=1080,
    viewport_height=600,
    text_mode=False,            # True=禁用图片，加速文本爬取
    light_mode=False,           # True=关闭部分后台功能
    enable_stealth=False,       # playwright-stealth反检测
    user_agent="...",           # 自定义UA
    user_agent_mode="random",   # 随机UA池
    proxy_config={"server": "http://proxy:8080", "username": "u", "password": "p"},
    cookies=[{"name": "session", "value": "...", "url": "..."}],
    headers={"Accept-Language": "zh-CN"},
    use_managed_browser=False,  # True=CDP持久化控制
    user_data_dir=None,         # 持久化目录(跨运行保持cookies/session)
    storage_state=None,         # dict或str，恢复cookies/localStorage
    ignore_https_errors=True,
    java_script_enabled=True,   # False=纯静态省资源
    device_scale_factor=1.0,    # 2.0=Retina截图(内存翻倍)
    extra_args=["--disable-extensions"],
)
```

**注意**: `use_persistent_context=True` 会自动设置 `use_managed_browser=True`

### CrawlerRunConfig — 每次爬取执行配置

```python
from crawl4ai import CrawlerRunConfig, CacheMode

run_cfg = CrawlerRunConfig(
    # 内容处理
    word_count_threshold=10,        # 忽略<10词文本块
    css_selector=".main-content",   # 只关注此区域
    excluded_tags=["form", "nav"],  # 移除整个标签块
    remove_overlay_elements=True,   # 移除弹窗/遮罩
    only_text=False,                # True=移除非文本元素

    # 链接处理
    exclude_external_links=True,
    exclude_social_media_links=True,

    # 页面导航和时序
    wait_for="css:.dynamic-content",   # "css:selector" 或 "js:() => boolean"
    delay_before_return_html=2.0,      # 捕获前等待秒数
    page_timeout=60000,                # 导航超时(ms)

    # JS执行 (执行顺序: js_code_before_wait → wait_for → delay → js_code)
    js_code=["window.scrollTo(0, document.body.scrollHeight);"],
    js_code_before_wait="document.querySelector('#tab')?.click();",
    js_only=False,                     # True=不重新导航，同一session执行JS
    session_id="my_session",           # 跨调用复用浏览器tab

    # 截图/PDF
    screenshot=True,                   # result.screenshot → base64
    screenshot_wait_for=1.0,
    pdf=True,                          # result.pdf → bytes

    # 反爬
    magic=True,                        # 综合stealth功能
    simulate_user=True,                # 模拟鼠标移动
    override_navigator=True,           # 伪装navigator属性

    # 缓存
    cache_mode=CacheMode.BYPASS,       # ENABLED|DISABLED|BYPASS|WRITE_ONLY|READ_ONLY
    check_robots_txt=True,

    # 提取策略
    extraction_strategy=None,          # 见下方

    # Markdown生成
    # markdown_generator=DefaultMarkdownGenerator(
    #     content_filter=PruningContentFilter(threshold=0.48),
    # ),

    # 深度爬取
    # deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2),

    # 并发(arun_many用)
    semaphore_count=5,
    mean_delay=0.1,
    max_range=0.3,
)
```

### CrawlResult — 返回结果

```python
result.success          # bool
result.status_code      # HTTP状态码
result.url              # 最终URL(含重定向)
result.markdown         # MarkdownGenerationResult
result.markdown.raw_markdown          # 原始markdown
result.markdown.fit_markdown          # 过滤后的精简markdown(最常用)
result.html             # 原始HTML
result.cleaned_html     # 清洗后HTML
result.extracted_content  # JSON字符串(结构化提取结果)
result.screenshot       # base64截图
result.pdf              # bytes PDF
result.media            # {"images": [...], ...}
result.links            # {"internal": [...], "external": [...]}
result.tables           # 表格数据
result.js_execution_result  # JS执行结果
result.error_message    # 错误信息
```

---

## 5大使用模式

### 模式1: 基础爬取 (Markdown输出)

```python
import asyncio, json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def crawl_basic(url):
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        result = await crawler.arun(url=url, config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=5,
        ))
        if result.success:
            return result.markdown.raw_markdown
        else:
            return f"Error: {result.error_message}"

# execute_code中调用:
# result = asyncio.run(crawl_basic("https://example.com"))
# print(result)
```

### 模式2: Stealth爬取 (反检测)

**级别A — playwright-stealth** (简单场景):
```python
browser_cfg = BrowserConfig(enable_stealth=True, headless=True)
async with AsyncWebCrawler(config=browser_cfg) as crawler:
    result = await crawler.arun(url="https://protected-site.com")
```

**级别B — Undetected模式** (深度反检测):
```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, UndetectedAdapter
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy

browser_cfg = BrowserConfig(headless=False, verbose=True)
adapter = UndetectedAdapter()
strategy = AsyncPlaywrightCrawlerStrategy(browser_config=browser_cfg, browser_adapter=adapter)
async with AsyncWebCrawler(crawler_strategy=strategy, config=browser_cfg) as crawler:
    result = await crawler.arun(url="https://cloudflare-protected.com")
```

**级别C — 最强组合** (Stealth + Undetected):
```python
browser_cfg = BrowserConfig(enable_stealth=True, headless=False)
adapter = UndetectedAdapter()
strategy = AsyncPlaywrightCrawlerStrategy(browser_config=browser_cfg, browser_adapter=adapter)
async with AsyncWebCrawler(crawler_strategy=strategy, config=browser_cfg) as crawler:
    result = await crawler.arun(url="https://hardcore-protected.com",
        config=CrawlerRunConfig(magic=True, simulate_user=True, override_navigator=True))
```

**渐进升级**: 普通模式 → +enable_stealth → +UndetectedAdapter → +headless=False+magic

### 模式3: 结构化提取

**A. JsonCssExtractionStrategy** (最快，零LLM成本):
```python
from crawl4ai import JsonCssExtractionStrategy

schema = {
    "name": "Articles",
    "baseSelector": "div.article",   # 重复容器
    "fields": [
        {"name": "title", "selector": "h2", "type": "text"},
        {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"},
        {"name": "image", "selector": "img", "type": "attribute", "attribute": "src"},
        {"name": "price", "selector": ".price", "type": "text", "transform": "strip"},
        {"name": "tags", "selector": ".tag", "type": "text", "multiple": True},
        {"name": "is_sponsored", "selector": ".sponsored", "type": "exists"},
        {"name": "date", "selector": "time", "type": "regex", "pattern": r"\d{4}-\d{2}-\d{2}"},
        # 嵌套字段
        {"name": "variants", "type": "nested", "selector": ".variant", "fields": [
            {"name": "color", "selector": ".color", "type": "text"},
            {"name": "price", "selector": ".price", "type": "text"},
        ]},
    ],
}
extraction = JsonCssExtractionStrategy(schema, verbose=True)
config = CrawlerRunConfig(extraction_strategy=extraction)
result = await crawler.arun(url="...", config=config)
data = json.loads(result.extracted_content)  # List[Dict]
```

**字段类型**: `text` | `attribute` | `html` | `regex` | `exists` | `nested` | `list`

**B. JsonXPathExtractionStrategy** (XPath版):
```python
from crawl4ai import JsonXPathExtractionStrategy

schema = {
    "name": "Items",
    "baseSelector": "//div[@class='item']",   # XPath
    "fields": [
        {"name": "title", "selector": ".//h2", "type": "text"},
        {"name": "link", "selector": ".//a", "type": "attribute", "attribute": "href"},
    ],
}
extraction = JsonXPathExtractionStrategy(schema)
```

**C. LLMExtractionStrategy** (语义提取，需LLM):
```python
from crawl4ai import LLMExtractionStrategy, LLMConfig
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float
    description: str

extraction = LLMExtractionStrategy(
    llm_config=LLMConfig(provider="openai/gpt-4o-mini", api_token="env:OPENAI_API_KEY"),
    schema=ProductInfo.model_json_schema(),
    extraction_type="schema",     # "schema"(结构化) | "block"(自由文本)
    instruction="Extract product information.",
    chunk_token_threshold=4000,
    input_format="markdown",      # "markdown" | "fit_markdown" | "html"
)
config = CrawlerRunConfig(extraction_strategy=extraction)
# 结果: json.loads(result.extracted_content) → List[ProductInfo dict]
# 提取后调用 extraction.show_usage() 查看token用量
```

**LLMConfig支持的provider格式**: `"openai/gpt-4o"`, `"ollama/llama2"`, `"anthropic/claude-3-sonnet"`, `"groq/mixtral"`, 任何LiteLLM支持的模型

**D. RegexExtractionStrategy** (正则提取):
```python
from crawl4ai.extraction_strategy import RegexExtractionStrategy

# 内置flag: Email|PhoneIntl|Url|IPv4|Currency|Percentage|DateIso|HexColor|All 等20+
strategy = RegexExtractionStrategy(
    pattern=RegexExtractionStrategy.Email | RegexExtractionStrategy.Url | RegexExtractionStrategy.Currency
)
# 自定义正则
strategy = RegexExtractionStrategy(custom={"usd_price": r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"})
```

**E. 两阶段提取** (一次LLM生成schema → 后续零LLM):
```python
# 阶段1: LLM生成schema(一次性)
strategy = JsonCssExtractionStrategy(schema=None, generate_schema=True)
result = await crawler.arun(url, config=CrawlerRunConfig(extraction_strategy=strategy))
saved_schema = strategy.generated_schema  # 保存此schema!

# 阶段2: 后续所有爬取用纯CSS，零LLM成本
fast_strategy = JsonCssExtractionStrategy(saved_schema)
```

**坑**: generate_schema可能生成脆弱的nth-child选择器。建议指定指令避免。

### 模式4: JS交互 + Session多步操作

```python
# 多步操作: 加载→点击→滚动→提取
session_id = "my_multi_step"

# Step 1: 加载初始页
config1 = CrawlerRunConfig(wait_for="css:.content", session_id=session_id)
result1 = await crawler.arun(url="https://example.com", config=config1)

# Step 2: 点击标签页(不重新导航)
config2 = CrawlerRunConfig(
    js_code_before_wait="document.querySelector('#specs-tab')?.click();",
    wait_for="css:#specs-panel .content",
    js_only=True,           # 关键: 不重新导航!
    session_id=session_id,  # 复用同一tab
)
result2 = await crawler.arun(url="...", config=config2)

# Step 3: 滚动加载更多
config3 = CrawlerRunConfig(
    js_code=["window.scrollTo(0, document.body.scrollHeight);"],
    wait_for="js:() => document.querySelectorAll('.item').length > 30;",
    js_only=True,
    session_id=session_id,
)
result3 = await crawler.arun(url="...", config=config3)

# 清理session
await crawler.crawler_strategy.kill_session(session_id)
```

**JS执行顺序**: `js_code_before_wait` → `wait_for` → `delay_before_return_html` → `js_code`

### 模式5: 批量爬取 + 深度爬取

**批量爬取 arun_many**:
```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher, RateLimiter

# 简单批量
results = await crawler.arun_many(
    urls=["https://site1.com", "https://site2.com"],
    config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
)

# 内存自适应+限速(生产推荐)
dispatcher = MemoryAdaptiveDispatcher(
    memory_threshold_percent=70.0,   # 内存超70%暂停
    max_session_permit=5,            # 最大并发
    rate_limiter=RateLimiter(base_delay=2.0, max_delay=10.0, max_retries=1),
)
results = await crawler.arun_many(urls=urls, config=cfg, dispatcher=dispatcher)

# 流式批量
async for result in await crawler.arun_many(
    urls=urls, config=CrawlerRunConfig(stream=True, cache_mode=CacheMode.BYPASS)
):
    process(result)
```

**深度爬取/Spider**:
```python
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, DomainFilter, URLPatternFilter
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

# BFS广度优先
config = CrawlerRunConfig(
    deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, include_external=False, max_pages=50),
    stream=True,
)

# BestFirst智能优先(推荐)
filter_chain = FilterChain([
    DomainFilter(allowed_domains=["docs.example.com"]),
    URLPatternFilter(patterns=["*guide*", "*tutorial*"]),
])
scorer = KeywordRelevanceScorer(keywords=["api", "config"], weight=0.7)

config = CrawlerRunConfig(
    deep_crawl_strategy=BestFirstCrawlingStrategy(
        max_depth=2, include_external=False,
        filter_chain=filter_chain, url_scorer=scorer, max_pages=25,
    ),
    stream=True,
)

async with AsyncWebCrawler() as crawler:
    async for result in await crawler.arun("https://example.com", config=config):
        print(f"[Depth {result.metadata.get('depth', 0)}] {result.url}")
```

---

## 截图 + PDF

```python
config = CrawlerRunConfig(screenshot=True, screenshot_wait_for=1.0, pdf=True)
result = await crawler.arun(url, config=config)

# 保存截图
from base64 import b64decode
if result.screenshot:
    with open("screenshot.png", "wb") as f:
        f.write(b64decode(result.screenshot))

# 保存PDF
if result.pdf:
    with open("page.pdf", "wb") as f:
        f.write(result.pdf)

# Retina截图(2x分辨率)
browser_cfg = BrowserConfig(device_scale_factor=2.0)
```

---

## Markdown内容过滤

```python
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter

# Pruning过滤 — 基于文本密度(阈值0.3-0.5，越高越严格)
config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.48),
        content_source="cleaned_html",
    )
)
# 结果: result.markdown.fit_markdown = 精简markdown

# BM25过滤 — 基于查询相关性
config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=BM25ContentFilter(user_query="machine learning", threshold=0.3),
    )
)
```

---

## Hooks系统 (8个钩子点)

```python
async def on_page_context_created(page, context, **kwargs):
    """最佳拦截点 — 阻止图片/字体/CSS加载(大幅加速)"""
    async def route_filter(route):
        if route.request.resource_type in ("image", "font", "stylesheet"):
            await route.abort()
        else:
            await route.continue_()
    await context.route("**", route_filter)
    return page

async def before_goto(page, context, url, **kwargs):
    """导航前 — 注入自定义headers"""
    await page.set_extra_http_headers({"Custom-Header": "value"})
    return page

crawler = AsyncWebCrawler(config=browser_config)
crawler.crawler_strategy.set_hook("on_page_context_created", on_page_context_created)
crawler.crawler_strategy.set_hook("before_goto", before_goto)
await crawler.start()
```

钩子点: `on_browser_created` → `on_page_context_created` → `before_goto` → `after_goto` → `before_retrieve_html` → `before_return_html`

---

## 高级技巧

### 1. 身份持久化爬取(登录后复用)

```python
# 方式1: 持久化目录
browser_cfg = BrowserConfig(use_managed_browser=True, user_data_dir="/path/to/profile")

# 方式2: storage_state恢复
browser_cfg = BrowserConfig(storage_state={
    "cookies": [{"name": "session", "value": "...", "domain": "example.com", "path": "/"}],
    "origins": [{"origin": "https://example.com", "localStorage": [{"name": "token", "value": "..."}]}]
})
```

### 2. 调试利器(捕获网络请求/控制台)

```python
config = CrawlerRunConfig(capture_network_requests=True, capture_console_messages=True)
result = await crawler.arun(url, config=config)
for req in result.network_requests:
    print(f"{req.get('method')} {req.get('url')} → {req.get('status')}")
```

### 3. raw:// 协议(直接处理HTML，不发网络请求)

```python
result = await crawler.arun(
    url="raw://<html><body><div class='item'>Hello</div></body></html>",
    config=CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema)),
)
```

### 4. CacheMode策略

| 模式 | 用途 |
|------|------|
| `BYPASS` | 开发调试，每次重新爬取 |
| `WRITE_ONLY` | 第一遍爬取，写入缓存 |
| `READ_ONLY` | 后续只读缓存，不重复下载 |
| `ENABLED` | 正常读写(默认) |

### 5. 内存管理最佳实践

```python
# ❌ 错误: 循环中重复创建crawler
for url in urls:
    async with AsyncWebCrawler() as crawler:
        await crawler.arun(url)

# ✅ 正确: 复用crawler
async with AsyncWebCrawler() as crawler:
    for url in urls:
        await crawler.arun(url)

# ✅ 批量用Dispatcher控制内存
dispatcher = MemoryAdaptiveDispatcher(memory_threshold_percent=70.0, max_session_permit=5)

# ✅ 及时kill sessions
await crawler.crawler_strategy.kill_session(session_id)
```

---

## Pitfalls (常见坑)

| 坑 | 解决方案 |
|------|----------|
| lxml版本冲突 | crawl4ai要求5.x，scrapling要求6.x。当前用6.1.0，两者实测都正常。如报错：不用LXMLWebScrapingStrategy，用默认WebScrapingStrategy |
| headless被检测 | 设 `headless=False` + `enable_stealth=True` |
| JS不执行 | 需要先触发的用 `js_code_before_wait`，不是 `js_code` |
| extracted_content为空 | 检查baseSelector在当前页是否存在；用 `verbose=True` 看日志 |
| 截图为None | 页面太大/超时，增大 `page_timeout`，或改用 `pdf=True` |
| Markdown包含广告 | 用 `PruningContentFilter` 或 `BM25ContentFilter`；设 `remove_overlay_elements=True` |
| session泄漏 | 用完必须 `kill_session(session_id)` |
| PruningContentFilter过于激进 | 降低threshold(0.3-0.5)；或改用BM25 |
| wait_for超时 | 检查JS是否已加载；增加 `page_timeout` |
| generate_schema生成脆弱选择器 | 避免nth-child，指定用href/data属性/class名的指令 |
| 内存泄漏(Docker) | 用MemoryAdaptiveDispatcher；设max_session_permit；Docker加 `--shm-size=1g` |
| SSL证书错误 | `BrowserConfig(ignore_https_errors=True)` |

---

## 与Scrapling的互补关系

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

---

## Guardrails

- 只爬取有权限访问的内容
- 遵守 robots.txt (`check_robots_txt=True`)
- 大规模爬取加延迟 (`RateLimiter`)
- 不绕过付费墙或认证（无授权情况下）
- 不爬取个人/敏感数据
