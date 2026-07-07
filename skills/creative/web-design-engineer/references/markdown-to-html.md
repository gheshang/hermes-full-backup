# Markdown → HTML 文档渲染指南

把结构化 Markdown（教程、文档、README）渲染为带导航的完善 HTML 页面。

## 通用渲染流程

```python
import markdown

html_body = markdown.markdown(
    md_text,
    extensions=['tables', 'fenced_code', 'codehilite', 'nl2br', 'toc']
)
```

### 常用扩展

| 扩展 | 用途 |
|------|------|
| `tables` | Markdown 表格 → HTML `<table>` |
| `fenced_code` | 代码块用 ``` 包围 |
| `codehilite` | 代码语法高亮 |
| `nl2br` | 换行转 `<br>`（中文文档密集段落保留换行） |
| `toc` | 生成标题锚点 ID |

---

## ⚠️ 关键陷阱：TOC 列表 ID 必须从渲染后的 HTML 提取

**不要自己用正则/字符串拼接生成目录链接的 `#id`。**

Python `markdown` 库的 `TocExtension` 自动分配标题 ID，其规则是：

1. 移除 HTML 标签
2. 只保留 ASCII 字母/数字/连字符
3. 连续非单词字符压缩为单个 `-`
4. 中文/CJK **被完全移除**（不可用于 ID）
5. 重复 ID 自动加 `_1`, `_2` 后缀

所以你手动从 markdown 原文生成 ID 的方式：
```python
# ❌ 这样做 ID 会不匹配！
item_id = re.sub(r'[^\w\u4e00-\u9fff]+', '-', item).lower().strip('-')
```

因为 markdown 库把中文全扔了，你保留了中文，出来的 ID 完全不同。

**✅ 正确做法：从渲染后的 HTML 提取真实 ID**

```python
md_converter = markdown.Markdown(
    extensions=['tables', 'fenced_code', 'codehilite', 'nl2br', 
                TocExtension(baselevel=1, separator='-')]
)
html_body = md_converter.convert(md_text)

# 提取 h2 的真实 ID
h2_pattern = re.compile(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>')
toc_items = []
for match in h2_pattern.finditer(html_body):
    h2_id = match.group(1)
    h2_text_clean = re.sub(r'<[^>]+>', '', match.group(2))
    toc_items.append((h2_id, h2_text_clean))

# 用真实 ID 生成 TOC 链接
toc_html = ''
for h2_id, text in toc_items:
    toc_html += f'<li><a href="#{h2_id}">{text}</a></li>\n'
```

---

## 侧边栏 TOC CSS 要点

```css
/* 固定侧边栏 */
.sidebar {
  width: 260px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
}

/* 移动端隐藏，加汉堡菜单按钮 */
@media (max-width: 768px) {
  .sidebar { display: none; }
  .sidebar.show { display: block; position: fixed; z-index: 999; }
}
```

---

## 表格横向滚动

Markdown 表格宽列在移动端会溢出，需要让 table 可横向滚动：

```css
.content table {
  display: block;
  overflow-x: auto;
}
```

---

## 样式平衡

| 元素 | 建议值 |
|------|--------|
| 正文字号 | 15-16px |
| 正文行高 | 1.7-1.8 |
| h1 字号 | 26-28px |
| h2 字号 | 20-22px |
| h3 字号 | 16-17px |
| 代码字号 | 13px |
| 侧边栏链接 | 13px |
| 正文最大宽度 | 800-880px |
| 总布局宽度 | 1300-1400px |