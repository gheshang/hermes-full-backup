# HTML+SVG 信息图生成指南

当需要可编辑、可缩放、文件小的信息图时，使用 HTML+内联 SVG 方案，而非 AI 生成的 PNG。

## 适用场景

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 文档嵌入（Markdown） | PNG | Markdown 原生支持，视觉效果好 |
| 网页展示 | HTML+SVG | 可编辑、可缩放、文件小 |
| 演示/打印 | PNG | 渲染一致，无需浏览器 |
| 开发/迭代 | HTML+SVG | 代码可改，即时反馈 |
| 文字密集图表 | HTML+SVG | 文字 100% 清晰 |
| 需要交互效果 | HTML+SVG | 支持 hover、动画等 |

## 核心结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>图表标题</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1664px;
      height: 1040px;
      background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 50%, #0d1326 100%);
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
      overflow: hidden;
    }
    /* 网格背景 */
    .grid {
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
      background-size: 40px 40px;
    }
    /* 语义化颜色 */
    .accent-cyan { --accent: #38bdf8; }
    .accent-emerald { --accent: #34d399; }
    .accent-violet { --accent: #a78bfa; }
    .accent-amber { --accent: #fbbf24; }
    .accent-rose { --accent: #f472b6; }
  </style>
</head>
<body>
  <div class="grid"></div>
  
  <!-- 内容 -->
  <div class="title">图表标题</div>
  <div class="cards">
    <div class="card">卡片内容</div>
  </div>
</body>
</html>
```

## SVG 连接线示例

```html
<svg class="connections" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none;">
  <defs>
    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" opacity="0.6"/>
    </marker>
  </defs>
  <!-- 曲线连接 -->
  <path d="M 832 240 Q 600 280 400 340" stroke="#38bdf8" stroke-width="2" fill="none" marker-end="url(#arrow-cyan)" opacity="0.4"/>
  <!-- 直线连接 -->
  <line x1="832" y1="260" x2="832" y2="300" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)" opacity="0.5"/>
</svg>
```

## 卡片组件模板

```html
<div class="card card-1">
  <div class="accent-bar"></div>
  <div class="card-icon">📊</div>
  <div class="card-content">
    <div class="card-title">卡片标题</div>
    <div class="card-desc">描述文字</div>
  </div>
</div>
```

```css
.card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 16px;
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--accent);
}
.card-icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  background: var(--accent-bg);
  color: var(--accent);
}
```

## 对比表格模板

```html
<div class="columns">
  <div class="column">
    <div class="product-header">
      <div class="icon">🚀</div>
      <div class="name">产品 A</div>
    </div>
    <div class="feature-row">
      <div class="feature-name">特性 1</div>
      <div class="status status-check">✓</div>
    </div>
    <div class="feature-row">
      <div class="feature-name">特性 2</div>
      <div class="status status-cross">✗</div>
    </div>
  </div>
</div>
```

```css
.status-check { color: #34d399; }
.status-cross { color: #f87171; opacity: 0.6; }
.status-partial { color: #fbbf24; }
```

## 生成工作流

1. **确定图表类型**（架构/流程/对比/网格/关系图）
2. **选择模板结构**（参考下方模板索引）
3. **编写 HTML+CSS**（保持语义化配色）
4. **添加 SVG 连接**（如需要）
5. **保存为 .html 文件**
6. **（可选）用浏览器截图生成 PNG**

## 模板索引

| 类型 | 模板文件 | 适用场景 |
|------|----------|----------|
| 封面/概览 | `templates/cover-grid.html` | 文档封面、生态概览 |
| 架构图 | `templates/architecture-diagram.html` | 系统架构、数据流 |
| 代理关系图 | `templates/agent-architecture.html` | 多代理协作、层级关系 |
| 工作流程图 | `templates/workflow-diagram.html` | 任务流程、步骤图 |
| 任务类别网格 | `templates/category-grid.html` | 分类展示、九宫格 |
| 对比图 | `templates/comparison-table.html` | 产品对比、特性比较 |

## 最佳实践

1. **语义化配色**：使用 CSS 变量定义颜色，便于主题切换
2. **响应式布局**：使用 Grid/Flexbox，适配不同尺寸
3. **文字清晰**：避免在 SVG 中渲染大量文字，用 HTML 元素
4. **性能优化**：内联 SVG，避免外部资源
5. **可访问性**：添加 `aria-label`，支持键盘导航
6. **暗色主题**：统一使用深色背景，符合技术文档风格

## 与 AI 生成 PNG 的协作

```
┌─────────────────────────────────────────────────────────┐
│                    双版本输出策略                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  需求分析 ──→ 选择方案 ──→ 生成 ──→ 交付               │
│     │            │           │          │               │
│     │            ├─ PNG ────┤          │               │
│     │            │          │          │               │
│     │            └─ HTML ───┤          │               │
│     │                       │          │               │
│     └─ 用户偏好 ────────────┘          │               │
│                                        │               │
│  文档嵌入 ─────────────────────────────→ PNG            │
│  网页展示 ─────────────────────────────→ HTML           │
│  可编辑需求 ───────────────────────────→ HTML           │
│  视觉优先 ─────────────────────────────→ PNG            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
