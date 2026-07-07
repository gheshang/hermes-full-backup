#!/usr/bin/env python3
"""清洗 PDF 转 Markdown 后的重复页眉页脚"""
import re
import sys

def clean_pdf_markdown(text):
    lines = text.split('\n')
    
    # ─── 可定制列表 ───
    page_num_pattern = re.compile(r'^- \d+ -$')           # "- 1 -", "- 2 -"
    footer_texts = ['中华人民共和国国家发展和改革委员会发布']
    header_texts = ['中华人民共和国国家发展和改革委员会规章']
    # 页眉后面紧跟的标题行（如 "供电营业规则"）
    title_texts  = ['供电营业规则']
    # ─────────────────

    result = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 跳过页码行
        if page_num_pattern.match(stripped):
            continue

        # 跳过页脚
        if stripped in footer_texts:
            continue

        # 跳过页眉
        if stripped in header_texts:
            continue

        # 跳过页眉后的标题
        if stripped in title_texts:
            lookback = 0
            for j in range(max(0, i-3), i):
                prev = lines[j].strip()
                if prev in header_texts or prev in footer_texts or page_num_pattern.match(prev):
                    lookback += 1
            if lookback > 0:
                continue

        # 跳过表格分隔线残留（| --- | --- | 或 --- | --- | 类）
        if '|' in stripped:
            # 去掉|和空格后只剩短横线 → 表格分隔线
            stripped2 = stripped.replace('|', '').replace(' ', '').replace('\t', '')
            if stripped2 and all(c == '-' for c in stripped2):
                continue

        result.append(line)
    
    # 合并多余空行
    cleaned = []
    empty_count = 0
    for line in result:
        if line.strip() == '':
            empty_count += 1
            if empty_count <= 1:
                cleaned.append(line)
        else:
            empty_count = 0
            cleaned.append(line)
    
    return '\n'.join(cleaned)


def main():
    if len(sys.argv) < 2:
        print("用法: clean-pdf-markdown.py <输入文件> [输出文件]")
        print("不指定输出文件则原地覆盖")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_lines = text.count('\n')
    original_len = len(text)
    
    cleaned = clean_pdf_markdown(text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    new_lines = cleaned.count('\n')
    new_len = len(cleaned)
    
    print(f"清洗完成:")
    print(f"  原文件: {original_lines} 行, {original_len} 字符")
    print(f"  清洗后: {new_lines} 行, {new_len} 字符")
    print(f"  删除:   {original_lines - new_lines} 行, {original_len - new_len} 字符")
    print(f"  输出:   {output_path}")


if __name__ == '__main__':
    main()
