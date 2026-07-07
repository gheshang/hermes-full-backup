---
name: open-source-source-dive
description: 从 GitHub 获取开源项目信息的完整方法论——包括源码直查、文档抓取、综合教程撰写与 Web 部署。当官方文档缺失细节、git clone 失败、或需要为工具编写教程时加载。
tags: [source-code, github, documentation, tutorial, web-deployment]
---

# 开源项目信息获取与教程撰写

## 触发条件
- 官方文档缺失关键细节（运算符列表、参数枚举、隐藏配置）
- GitHub 代码搜索需登录无法使用
- `git clone` 超时/断连（网络受限环境），需改用文档抓取
- web_extract 抓 raw.githubusercontent.com 返回 404（路径猜不准）
- 用户要求为某个开源工具编写详尽教程（含 Web 部署以便移动端阅读）

## 两条路径：按需选择

| 路径 | 目标 | 适用场景 |
|------|------|---------|
| **A: 源码直查** | 获取代码级精确答案 | 官方文档不全，需要确认实现细节 |
| **B: 文档抓取→教程** | 获取完整文档（README/FAQ/SKILL.md 等）→ 综合为教程 | git clone 超时；需要覆盖工具全部使用场景 |

---

## 路径 A：源码直查

### 标准流程

1. **浅克隆目标仓库**
   ```bash
   cd /tmp && git clone --depth 1 <repo-url>
   ```

2. **关键词定位文件**
   ```bash
   grep -rl '<keyword>' --include='*.py' --include='*.js' --include='*.ts' src/
   ```

3. **读核心文件**
   - 运算符/枚举 → `constants`、`shared`、`enum`、`types` 文件
   - 条件逻辑 → `handler`、`test`、`validate`、`builder` 文件
   - UI选项 → `locale`、`i18n`、组件文件

4. **交叉验证**：定义层 + 声明层 + 展示层三方对照

5. **清理**：`rm -rf /tmp/<repo-name>`

### 踩坑记录

- **GitHub raw URL 404**：不要猜路径，直接 clone 后用 grep
- **GitHub 代码搜索需登录**：克隆本地 grep 是可靠替代
- **npm/pip 包不完整**：浏览器扩展类项目逻辑散布在多上下文，包只是子集

---

## 路径 B：文档抓取与教程撰写

### 第一步：GitHub 文档抓取（替代 clone）

当 `git clone` 超时时，改用 `web_extract` 逐个抓取 GitHub 文档文件：

**URL 模式**：`https://github.com/<org>/<repo>/blob/main/<路径>`

**抓取顺序**（三轮递进）：

| 轮次 | 抓取目标 | 示例 URL |
|------|---------|----------|
| 第 1 轮 | README（中英文） | `.../blob/main/README.md`, `README_CN.md` |
| 第 2 轮 | 核心文档（根据 README 导航表） | `docs/zh/getting-started.md`, `docs/zh/faq.md`, `docs/zh/technical-design.md`, `docs/zh/why-ppt-master.md` |
| 第 3 轮 | 技术参考（SKILL.md、脚本、参考） | `skills/ppt-master/SKILL.md`, `skills/ppt-master/scripts/README.md`, `skills/ppt-master/references/canvas-formats.md` |

**关键参数**：`web_extract(urls=[...], char_limit=25000)` — 设置 25000 字符限制避免大文档被截断。对超过 15K 字符的页面，web_extract 会自动保存完整文件到 cache，用 `read_file` 分页读取中间部分。

**可并行抓取**：同一轮次内的 URL 无依赖关系，一次 `web_extract` 调用最多 5 个 URL。

### 第二步：综合教程撰写

将 5–15 个来源文档合成为一篇结构清晰的教学文档：

**合成原则**：
1. **按使用流程组织**——用户从"安装→配置→快速上手→进阶→FAQ"的自然顺序学习，而非按源文件组织
2. **去重合并**——同一信息出现在多个文档中时只写一次
3. **保留技术细节**——命令、配置项、参数表、对比表原样保留
4. **补充上下文连线**——多个文档间的依赖关系显式说明
5. **分类 FAQ**——将分散的常见问题聚合到统一章节

**章节结构模板**（根据项目复杂度增减）：
```
1. 工具是什么 / 核心概念与路线
2. 与其他方案对比（表格）
3. 环境准备
4. 安装与配置
5. 快速上手（最短路径）
6. 核心工作流详解
7. [专项功能：图片/模板/脚本等]
8. 高级技巧
9. 脚本/工具速查表
10. 常见问题（Q&A 格式）
11. 错误排查与恢复
```

**代码块规范**：
- shell 命令用 `bash` 标注
- 配置文件用对应语言标注
- 用户与 AI 对话示例用 `text` 标注
- 所有命令必须是真实可验证的

### 第三步：Web 部署（移动端/平板查看）

当用户需要在浏览器中查看教程时，将 Markdown 转为 HTML 并启动 HTTP 服务：

```bash
# 1. Python markdown 库转换（先确认 markdown 包已装）
python3 -c "import markdown; print('ok')"

# 2. 生成带样式和侧边栏目录的 HTML
# 使用 extensions=['tables','fenced_code','codehilite','toc']
# 自动从 markdown 的 ## 标题提取目录

# 3. 启动 HTTP 服务
cd <输出目录> && python3 -m http.server <端口>
```

**HTML 样式要点**：深色代码块、表格条纹、blockquote 左色条、响应式（小屏隐藏侧边栏）、`<meta name="viewport">` 启用移动缩放。

**端口选择**：避开冲突端口（nginx 80、jupyter 18080），用 8765/8080 等高端口。用 `ss -tlnp | grep <端口>` 确认已绑定 `0.0.0.0`。

**nginx 替代**：若有 sudo 权限，直接复制到 `/var/www/html/` 通过 80 端口访问更稳定。

### 清理
```bash
process(action='kill', session_id='<id>')  # 停止 HTTP 服务
```

## 两条路径通用原则

- **没有调查就没有发言权**：路径 A 没 clone 过就别下源码结论，路径 B 没跑过验证就别交付
- **抓主要矛盾**：10 个文档里先读 README，它决定其余 9 个哪些值得读
- **一分为二**：文档里的 "Non-goals" 和 "Limitations" 往往比功能介绍更有价值