# Markdown → Jupyter Notebook 转换指南

用于把 Python 教程/题库 repo（如 Python-100-Days）转成可交互的 .ipynb 格式，方便学员在 Jupyter 上边看边练。

## 适用场景

- 代码教程以 Markdown 文件组织（.md），内含 ` ```python ` fenced code blocks
- 想把这些文档转成 Jupyter Notebooks，学员直接打开 Notebook 按 Shift+Enter 逐段运行
- 不适用：纯概念文档（无代码块的文件会变成单个 markdown cell，跟直接看 md 没区别）

## 前置条件

- Jupyter 已安装（自动带了 nbformat 依赖）
- Python-100-Days 已克隆到本地

## 操作步骤

```bash
# 1. 转换（源目录 → 输出目录）
python3 ~/.hermes/skills/devops/vps-python-dev-env/scripts/md-to-ipynb.py \
  /path/to/python-100-days \
  /path/to/jupyter/nb/

# 2. 指定只转某些章节（可选）
python3 ~/.hermes/skills/devops/vps-python-dev-env/scripts/md-to-ipynb.py \
  /path/to/python-100-days \
  /path/to/jupyter/nb/ \
  --dirs Day01-20,Day21-30

# 3. 确保 Jupyter 的 root_dir 包含 nb/
#    默认 root_dir 是 ~/python-practice，所以 nb/ 放在下面即可
```

## 转换结果

每篇 .md → 一个 .ipynb，保持目录结构。效果：

| .md 文件 | .ipynb 文件 | 单元格数 |
|---------|------------|---------|
| 04.Python语言中的运算符.md | 04.Python语言中的运算符.ipynb | ~23 个（11 代码 + 12 文本）|
| 概念性文章纯介绍.md | 概念性文章纯介绍.ipynb | 1 个（纯文本）|

## 已知限制

- **Indented code blocks（4空格缩进）**：Python-100-Days 偶尔有这种写法，当前脚本不处理，它们会留在 markdown cell 中作为展示。如果需要拆分，需增强 regex 或换用 jupytext
- **图片路径**：图片用 `<img src="res/day01/xxx.png">` 相对路径，保持源目录结构即可正常显示
- **公开课目录**：Python-100-Days 的 `公开课/` 目录下是独立目录结构（每节课一个子目录），转换时需要单独处理
- **nbformat 版本**：脚本生成的是 notebook v4 格式，Jupyter 2.x 和 Notebook 7.x 都兼容
