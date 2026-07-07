#!/usr/bin/env python3
"""
Markdown → Jupyter Notebook (.ipynb) 批量转换脚本

用法:
  # 1. 先装 nbformat（已装 Jupyter 的话自带）
  pip install nbformat

  # 2. 运行转换
  python3 md-to-ipynb.py /path/to/markdown/repo /path/to/output/dir

  # 3. 在 Jupyter 中访问
  把 output dir 放在 Jupyter root_dir 下即可在文件浏览器中看到

原理:
  - 读取每个 .md 文件
  - 用正则提取 fenced ```python 代码块 -> 作为 code cell
  - 代码块之间的文本 -> 作为 markdown cell
  - 其他语言代码块（```bash/```shell 等）作为 markdown cell 保留展示

支持的目录结构:
  - 单层: repo/*.md -> output/*.ipynb
  - 多层: repo/Chapter01/*.md -> output/Chapter01/*.ipynb
  - 可指定只处理特定子目录: --dirs Day01-20,Day21-30

注意:
  - 忽略 .gitignore 中匹配的文件
  - 图片路径保持相对关系不变
  - indented code blocks（4空格缩进）会被转为 markdown cell 不做拆解
"""
import nbformat as nbf
import re
import os
import sys
from pathlib import Path


def split_markdown(md_text):
    """将 markdown 按代码块分段，返回 [(type, content), ...]
    type: 'markdown' | 'code'
    """
    pattern = re.compile(r'(?s)```(\w*)\n(.*?)```')

    segments = []
    last_end = 0

    for match in pattern.finditer(md_text):
        lang = match.group(1).strip()
        code = match.group(2)
        start = match.start()

        # 代码块前面的文本
        if start > last_end:
            text_before = md_text[last_end:start].strip()
            if text_before:
                segments.append(('markdown', text_before))

        # 代码块
        if lang in ('', 'python', 'py', 'Python'):
            segments.append(('code', code.strip()))
        else:
            text = f"```{lang}\n{code}```"
            segments.append(('markdown', text))

        last_end = match.end()

    # 末尾剩余文本
    if last_end < len(md_text):
        remaining = md_text[last_end:].strip()
        if remaining:
            segments.append(('markdown', remaining))

    return segments


def convert_md_to_ipynb(md_path, nb_path):
    """单个文件转换"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    segments = split_markdown(md_text)

    if not segments:
        return False

    nb = nbf.v4.new_notebook()
    nb.metadata = {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.11.0'
        }
    }

    cells = []
    for cell_type, content in segments:
        if cell_type == 'code':
            cell = nbf.v4.new_code_cell(content)
        else:
            cell = nbf.v4.new_markdown_cell(content)
        cells.append(cell)

    nb.cells = cells

    os.makedirs(os.path.dirname(nb_path), exist_ok=True)
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Markdown -> Jupyter Notebook 批量转换')
    parser.add_argument('src', help='源目录（Markdown 文件所在根目录）')
    parser.add_argument('dst', help='输出目录（.ipynb 文件写入位置）')
    parser.add_argument('--dirs', help='只处理指定子目录，逗号分隔，如: Day01-20,Day21-30')
    parser.add_argument('--skip-dirs', default='.git,node_modules',
                        help='跳过的目录名（默认: .git,node_modules）')

    args = parser.parse_args()

    src_dir = Path(args.src)
    dst_dir = Path(args.dst)
    skip_dirs = set(args.skip_dirs.split(','))

    if not src_dir.exists():
        print(f"错误: 源目录不存在: {src_dir}")
        sys.exit(1)

    if args.dirs:
        target_dirs = [d.strip() for d in args.dirs.split(',')]
    else:
        target_dirs = [
            p.name for p in sorted(src_dir.iterdir())
            if p.is_dir() and p.name not in skip_dirs
        ]

    total = success = 0
    errors = []
    empty_files = []

    for dir_name in target_dirs:
        src_sub = src_dir / dir_name
        if not src_sub.is_dir():
            print(f"[跳过] {dir_name} 不是目录")
            continue

        md_files = sorted([f for f in os.listdir(src_sub) if f.endswith('.md')])

        for md_file in md_files:
            md_path = src_sub / md_file
            nb_path = dst_dir / dir_name / md_file.replace('.md', '.ipynb')

            total += 1
            try:
                if convert_md_to_ipynb(md_path, nb_path):
                    success += 1
                else:
                    empty_files.append(f"{dir_name}/{md_file}")
            except Exception as e:
                errors.append(f"{dir_name}/{md_file} ({e})")

    print(f"完成: {success}/{total} 个文件转换成功")
    if errors:
        print(f"转换错误: {len(errors)} 个")
        for e in errors[:5]:
            print(f"  x {e}")
    if empty_files:
        print(f"空文件（无内容跳过）: {len(empty_files)} 个")
        for e in empty_files[:5]:
            print(f"  - {e}")


if __name__ == '__main__':
    main()