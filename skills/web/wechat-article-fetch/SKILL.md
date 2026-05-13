---
name: wechat-article-fetch
description: 抓取微信公众号文章内容的方法论，绕过验证码和防爬机制。
version: 1.0
metadata:
  hermes:
    tags: [wechat, scraping, article, bypass]
---

# 微信公众号文章抓取

## 触发条件
需要读取微信公众号（mp.weixin.qq.com）文章内容。

## 方法（按优先级）

### 1. 移动端 User-Agent + requests
微信文章对移动端 UA 宽松得多。用 Android UA 直接 requests.get 通常能拿到完整 HTML：

```python
import requests, re, html

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
r = requests.get(url, headers=headers, timeout=15)
```

### 2. 浏览器工具
移动端 UA 仍可能触发验证码。浏览器工具（browser_navigate）打开后如果出现"环境异常"验证页面，基本无法绕过——需要滑动验证码，自动化工具搞不定。

### 3. Jina Reader API（备选）
`https://r.jina.ai/<url>` — 免费的网页转文本服务，但微信文章成功率不高。

## 正文提取

微信文章正文在 `id="js_content"` 的 div 中：

```python
m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', r.text, re.DOTALL)
raw = m.group(1) if m else r.text
clean = re.sub(r'<[^>]+>', '\n', raw)
clean = html.unescape(clean)
clean = re.sub(r'\n{3,}', '\n\n', clean).strip()
```

## 结论
移动端 UA + requests 是最可靠的方式，成功率约 80%。浏览器工具大概率被验证码拦截。
