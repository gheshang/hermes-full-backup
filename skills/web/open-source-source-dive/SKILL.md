---
name: open-source-source-dive
description: 当官方文档不完整或缺少细节（如运算符列表、配置项、隐藏功能）时，直接克隆仓库读源码获取权威答案的方法论。
tags: [source-code, github, reverse-engineering, documentation-gap]
---

# 开源项目源码直查

## 触发条件
- 官方文档缺失关键细节（运算符列表、参数枚举、隐藏配置）
- GitHub 代码搜索需登录无法使用
- web_extract 抓 raw.githubusercontent.com 返回 404（路径猜不准）
- 社区讨论只有模糊描述，无法确认版本准确性

## 标准流程

1. **浅克隆目标仓库**
   ```bash
   cd /tmp && git clone --depth 1 <repo-url>
   ```
   `--depth 1` 只取最新快照，省带宽省时间。

2. **关键词定位文件**
   ```bash
   grep -rl '<keyword>' --include='*.js' --include='*.vue' --include='*.ts' --include='*.py' src/
   ```
   同时搜多个关键词用 `\|` 连接。

3. **读核心文件**
   - 运算符/枚举 → 找 `constants`、`shared`、`enum`、`types` 文件
   - 条件逻辑 → 找 `handler`、`test`、`validate`、`builder` 文件
   - UI选项 → 找 `locale`、`i18n`、组件 `.vue` 文件

4. **交叉验证**
   - 运算符定义（逻辑层）+ compareTypes（声明层）+ UI组件（展示层）三方对照
   - 确认功能确实存在且未被条件编译移除

5. **清理**
   ```bash
   rm -rf /tmp/<repo-name>
   ```

## 踩坑记录

### GitHub raw URL 404
- `raw.githubusercontent.com/<org>/<repo>/<branch>/src/...` 路径猜不对就 404
- 不要猜路径，直接 clone 后用 grep 定位

### GitHub 代码搜索需登录
- `github.com/search?q=repo:...+keyword&type=code` 未登录返回空
- 克隆本地 grep 是可靠替代

### 文档只写"怎么用"不写"有什么"
- Automa 文档列出条件类型（Value/Code/Element），但不列出具体比较运算符
- 这种信息只在源码的常量定义里

### npm 包可能有用但不够
- `@automa-app/core` npm 页面看不到源码细节
- 浏览器扩展类项目，逻辑散布在 background/content/popup 多个上下文，npm 包只是子集

## 适用场景
- Chrome/Firefox 扩展功能确认
- Node.js 库的隐藏配置项
- Python 包的未文档化参数
- 任何文档滞后于代码的开源项目
