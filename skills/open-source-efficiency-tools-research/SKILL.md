# 开源工具调研 Skill

> 用于系统性爬取全网开源可本地部署的效率工具，按用户约束条件筛选并输出结构化报告。

---

## 一、需求澄清（必做，不可跳过）

在开始爬取前，必须确认以下 7 个维度：

### 1.1 约束条件确认

| # | 问题 | 说明 |
|---|------|------|
| 1 | 网络环境 | 纯内网 / 可外网 / 混合？Air-gapped 还是仅无公网 IP？ |
| 2 | 硬件平台 | Windows / Linux / macOS / 统信 UOS？CPU / GPU 配置？ |
| 3 | 权限限制 | 管理员权限？USB 设备？软件安装限制？ |
| 4 | 数据源 | 需要抓取哪些系统/网页？有 API 还是必须模拟 UI？ |
| 5 | 认证方式 | U 盾 / 短信验证码 / 账号密码 / 免认证？ |
| 6 | 输出目标 | 内网 AI 接口格式？IM 系统（企微/飞书/钉钉）？工单系统？ |
| 7 | 文档格式 | 规章制度文件格式比例（PDF/Word/图片）？更新频率？ |

### 1.2 调研范围确认

| # | 问题 | 说明 |
|---|------|------|
| 8 | 效率领域 | 网页采集 / 文档解析 / 本地 AI / RAG / 调度容错 / 工作流 / 其他？ |
| 9 | 输出深度 | A(清单) / B(分类报告) / C(深度评测)？ |
| 10 | 数量目标 | 30 / 50 / 100 / 不限？ |
| 11 | 评测方式 | 外网验证 / 文档分析 / 混合模式？ |
| 12 | 语言偏好 | 中文项目优先 / 英文也可 / 仅中文？ |

### 1.3 澄清流程

```
1. 用户说明处境 → 2. 助手总结约束 → 3. 用户确认/修正 → 4. 开始爬取
```

**关键原则：** 约束不确认，绝不开始爬取。每个约束直接影响技术选型。

---

## 二、爬取流程

### 2.1 搜索策略

**多源交叉验证，避免单一来源偏差：**

| 来源 | 用途 | 示例查询 |
|------|------|---------|
| GitHub Search | 项目主源 | `topic:self-hosted topic:python language:python` |
| GitHub Topics | 分类发现 | `python-playwright`, `rpa-robots`, `wecom` |
| Awesome Lists |  curated 列表 | `awesome-selfhosted`, `awesome-productivity` |
| Reddit | 真实用户测评 | `r/selfhosted`, `r/LocalLLaMA` |
| Hacker News | 技术讨论 | "show HN" + 工具名 |
| 技术博客 | 深度评测 | Firecrawl Blog, Bright Data, Medium |
| 基准测试 | 性能对比 | "Firecrawl vs Crawl4AI vs Spider benchmark" |

### 2.2 搜索关键词模板

```
# 网页自动化
"GitHub open source self-hosted web automation scraping Playwright Python"

# 文档解析
"GitHub open source document parsing PDF OCR MinerU Docling offline"

# 本地 AI
"GitHub open source local AI LLM self-hosted Ollama private deployment"

# RAG
"GitHub open source local RAG self-hosted SiYuan Obsidian private"

# 企业微信
"GitHub open source WeChat work enterprise WeCom bot API automation Python"

# 任务调度
"GitHub open source retry framework Python task scheduler fault tolerance"

# 综合列表
"GitHub awesome self-hosted productivity tools automation list"
```

### 2.3 信息提取字段

每个项目必须提取以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| 项目名称 | 官方名称 | Playwright |
| GitHub URL | 仓库链接 | https://github.com/microsoft/playwright |
| 介绍 | 一句话描述 | Microsoft 出品，跨平台网页自动化框架 |
| 测评摘要 | 来自社区/博客的关键评价 | 87k+ stars，行业标准，但浏览器二进制需首次下载 |
| 内网适配度 | ⭐ 1-5 评分 | ⭐⭐⭐⭐⭐ |
| 许可证 | MIT / Apache / GPL / Fair-code | MIT |
| 语言 | Python / Go / JS / Rust | Python |
| 部署方式 | pip / Docker / 源码编译 / 二进制 | pip + 首次下载浏览器 |
| 外网依赖 | 首次安装是否需要外网 | 是（浏览器二进制） |
| 跨平台 | Windows / Linux / macOS | 全平台 |

### 2.4 筛选规则

| 规则 | 说明 |
|------|------|
| ✅ 优先 | 纯 Python / 本地部署 / 开源许可 / 活跃维护（近 1 年） |
| ⚠️ 注意 | 需首次外网下载 / Fair-code 许可 / 社区较小 |
| ❌ 排除 | 强依赖云服务 / 闭源 / 无维护 / 仅 Windows |

---

## 三、整理规范

### 3.1 分类结构

```
一、网页自动化采集（P0）
二、文档解析与知识库（P0）
三、本地 AI 推理（P0）
四、RAG 与知识检索（P0）
五、任务调度与容错（P1）
六、企业微信集成（P1）
七、工作流自动化（P2）
八、其他效率工具（P2）
九、内网约束适配总结
十、推荐技术栈组合
十一、测评来源
```

### 3.2 表格格式

每个分类使用统一表格：

| # | 项目名称 | GitHub | 介绍 | 测评摘要 | 内网适配度 |
|---|---------|--------|------|---------|-----------|
| 1 | **Playwright** | microsoft/playwright | ... | ... | ⭐⭐⭐⭐⭐ |

### 3.3 适配度评分标准

| 星级 | 标准 |
|------|------|
| ⭐⭐⭐⭐⭐ | 完全离线，无外网依赖，跨平台完美 |
| ⭐⭐⭐⭐ | 首次需外网下载，之后完全离线 |
| ⭐⭐⭐ | 需额外依赖（Redis/Docker），但可内网部署 |
| ⭐⭐ | 部分功能需外网，或平台支持有限 |
| ⭐ | 强依赖云服务，不推荐内网使用 |

### 3.4 输出文档结构

```markdown
# [调研主题] 调研报告

> 约束条件：[列出关键约束]

## 一、网页自动化采集（P0）
[表格]

## 二、文档解析与知识库（P0）
[表格]

...

## 九、内网约束适配总结
[分类总结：完全适配 / 需外网初始化 / 不推荐]

## 十、推荐技术栈组合
[架构推荐图 + 文字说明]

## 十一、测评来源
[列出所有信息来源]
```

---

## 四、质量检查清单

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 1 | 需求已确认 | 7 个约束 + 6 个范围问题已回答 |
| 2 | 多源验证 | 每个项目至少 2 个信息来源 |
| 3 | 内网适配 | 每个项目标注内网适配度 |
| 4 | 约束覆盖 | 所有约束条件在适配总结中覆盖 |
| 5 | 推荐合理 | 推荐技术栈与约束一致 |
| 6 | 来源可追溯 | 所有测评摘要注明来源 |
| 7 | 格式统一 | 表格、星级、分类格式一致 |

---

## 五、增量更新流程

当需要新增项目时：

```
1. 确认新增领域（是否已有覆盖）
2. 按相同搜索策略爬取
3. 按相同表格格式添加
4. 更新适配总结
5. 更新推荐技术栈（如需要）
```

---

## 六、注意事项

### 6.1 内网环境特殊处理

- **Python 包**：外网 `pip download` → 内网 `pip install --no-index --find-links`
- **Docker 镜像**：外网 `docker pull` → `docker save` → 内网 `docker load`
- **Ollama 模型**：外网 `ollama pull` → 内网传输 `.bin` 文件
- **Playwright 浏览器**：外网 `playwright install` → 内网传输浏览器二进制

### 6.2 许可证注意

| 许可证 | 内网使用 | 说明 |
|--------|---------|------|
| MIT / Apache 2.0 | ✅ 无限制 | 最宽松 |
| GPL / AGPL | ✅ 内部使用无限制 | 修改需开源，内部使用不触发 |
| Fair-code (n8n) | ✅ 内部使用无限制 | 商业售卖需付费 |
| SSPL | ⚠️ 注意 | 云服务需授权 |

### 6.3 避免踩坑

- **不要只依赖 GitHub README**：社区测评（Reddit/博客）更真实
- **不要只看 stars**：小项目可能更专注特定场景
- **不要忽略许可证**：企业内网需注意合规
- **不要假设离线可行**：每个项目单独验证外网依赖

---

> Skill 版本：v1.0 | 创建时间：2026-05-15 | 适用场景：开源工具调研
