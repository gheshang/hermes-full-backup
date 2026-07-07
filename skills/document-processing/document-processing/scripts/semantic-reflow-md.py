#!/usr/bin/env python3
"""
语义重构：PDF→Markdown 知识库清洗（高阶）
流程：去管道符 → 合并硬断行 → 按章/条拆分 → 每条款独立段落

用法：
  python semantic-reflow-md.py 输入.md 输出.md
"""
import re
import sys

def clean_pipes(s):
    """去掉行内表格管道符和多余空格"""
    s = re.sub(r'\s*\|\s*', ' ', s)
    s = re.sub(r' {2,}', ' ', s)
    return s.strip()

def is_章(line):
    return bool(re.match(r'^第[一二三四五六七八九十百]+章', line))

def is_条(line):
    # "零"必须包含——"第一百零一条"的"零"不在常见数字字符里
    return bool(re.match(r'^第[一二三四五六七八九十百零]+条', line))


def semantic_reflow(text):
    lines = text.split('\n')

    # 1. 清洗管道符
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            cleaned.append('')
        else:
            cleaned.append(clean_pipes(s))

    # 2. 段落合并（只有章/条/空行是分段边界）
    paragraphs = []
    current = ''
    current_type = None

    for line in cleaned:
        if not line:
            if current:
                paragraphs.append((current_type or '续', current))
                current = ''
                current_type = None
            continue

        if is_章(line):
            if current:
                paragraphs.append((current_type or '续', current))
            paragraphs.append(('章', line))
            current = ''
            current_type = None
            continue

        if is_条(line):
            if current:
                paragraphs.append((current_type or '续', current))
            current = line
            current_type = '条'
            continue

        # 续行
        if current:
            current += ' ' + line
        else:
            current = line
            current_type = '续'

    if current:
        paragraphs.append((current_type or '续', current))

    # 3. 段落内拆分（有些段落粘了多条条款）
    final = []
    for ptype, ptext in paragraphs:
        ptext = re.sub(r'\s+', ' ', ptext).strip()

        if ptype == '章':
            final.append(('章', ptext))
        else:
            parts = re.split(r'(?=第[一二三四五六七八九十百零]+条)', ptext)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if is_条(part):
                    final.append(('条', part))
                else:
                    if final and final[-1][0] in ('条', '续'):
                        prev_type, prev_text = final[-1]
                        final[-1] = (prev_type, prev_text + ' ' + part)
                    else:
                        final.append(('续', part))

    # 4. 格式化输出
    output_lines = []
    for ptype, ptext in final:
        if ptype == '章':
            if output_lines and output_lines[-1] != '':
                output_lines.append('')
            output_lines.append(ptext)
            output_lines.append('')
        else:
            if output_lines and output_lines[-1] == '':
                output_lines.append(ptext)
            else:
                if output_lines:
                    output_lines.append('')
                output_lines.append(ptext)

    while output_lines and output_lines[0] == '':
        output_lines.pop(0)

    return '\n'.join(output_lines)


def main():
    if len(sys.argv) < 2:
        print("用法: semantic-reflow-md.py <输入.md> [输出.md]")
        print("不指定输出则用 '输入_reflowed.md'")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.md', '_reflowed.md')

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    original_lines = text.count('\n')
    original_len = len(text)

    output = semantic_reflow(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    new_lines = output.count('\n')
    new_len = len(output)

    print(f"语义重构完成:")
    print(f"  原文件: {original_lines} 行, {original_len} 字符")
    print(f"  重构后: {new_lines} 行, {new_len} 字符")
    print(f"  减少:   {original_lines - new_lines} 行, {original_len - new_len} 字符")
    print(f"  输出:   {output_path}")


if __name__ == '__main__':
    main()