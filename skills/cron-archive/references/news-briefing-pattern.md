# LLM 驱动定时新闻简报模式

## 适用场景

每天早上定时从多个全球新闻源采集热点新闻，翻译为中文，推送至飞书/微信等平台。

## 模式：纯 LLM 驱动（prompt + skills）

适用于需要"判断"的任务——AI 决定哪些新闻重要、如何排序、怎么翻译。

### 核心配置

```python
cronjob(
    action='create',
    name='每日全球新闻早报',
    prompt='''今天是 $(date +%Y年%m月%d日)。执行以下任务，全部用中文输出：

### 任务一：采集全球热门新闻
1. 访问 AP News (https://apnews.com) 获取头条，提取前 5 条
2. 访问 BBC World (https://www.bbc.com/news/world) 获取头条，提取前 5 条
3. 访问 The Guardian (https://www.theguardian.com/international) 获取头条，提取前 5 条
4. 访问 Reuters (https://www.reuters.com) 获取头条，提取前 3 条

### 任务二：采集 AI 热门新闻
1. 访问 Reuters AI (https://www.reuters.com/technology/artificial-intelligence)
2. 搜索 "top AI news today" 获取最新 AI 动态
选出全球最火的 3 条 AI 新闻

### 任务三：编译输出（严格按此格式）

🌏 **全球新闻早报 | $(date +%Y年%m月%d日)**

### 📡 AP News 热门
1. **标题**（中文翻译）
   🔗 原文链接

### 🤖 AI 焦点
1. **标题**（中文翻译）
   摘要：50-80字
   🔗 原文链接

要求：所有翻译成中文，附原文链接，AI 新闻有摘要，
总长度 ≤ 3000 字。''',
    schedule='30 7 * * *',   # 每天 7:30 北京时间
    deliver='feishu',
    enabled_toolsets=['web', 'terminal']
)
```

### 选择新闻来源的原则

| 来源 | 理由 | 备用 |
|------|------|------|
| AP News | 通讯社龙头，事实性报道 | 偶尔反爬，跳过即可 |
| BBC | 全球最受信任的品牌之一 | 稳定可访问 |
| The Guardian | 深度报道，国际视野 | 稳定可访问 |
| Reuters | 全球最大多媒体新闻商 | 动态加载，提取可能受限 |

### 输出格式要点

```
🌏 全球新闻早报 | 2026年7月6日

### 📡 AP News 热门
1. **伊朗最高领袖葬礼——德黑兰万人送行**
   🔗 https://apnews.com/article/...

### 🤖 AI 焦点
1. **Grok 4.5 进入 SpaceX 内部测试**
   摘要：马斯克宣布 1.5T 参数模型进入内部测试...
   🔗 https://...
```

### 重要提示

1. **prompt 必须自包含** — cron 任务在全新会话中运行，无历史上下文
2. **用 `$(date)` 动态获取日期** — 确保每天显示正确的日期
3. **用 `enabled_toolsets=['web']`** — 限制工具集节省 token
4. **网站访问失败时自我修复** — 在 prompt 中写明"如果不能访问则跳过"
5. **输出不要超过 3000 字** — 太长会被飞书截断或阅读体验差
6. **`deliver='feishu'` 交付** — 确保 cron 结果推送至飞书 Home 频道
7. **先手动 `cronjob run` 测试** — 等排期太慢，第一次务必手动触发验证

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 新闻内容为空 | 网站反爬/动态加载 | prompt 写明"访问失败则跳过该来源" |
| 输出过长被截断 | 超过飞书消息长度限制 | 限制每条摘要 50 字以内，总条数 ≤ 20 |
| 日期显示错误 | cron 运行 vs 写入时的时区差 | 用 `$(date...)` 而非硬编码写入 |
| 链接打不开 | 复制了截断的 URL | 确保提取完整的 URL（结尾无省略） |