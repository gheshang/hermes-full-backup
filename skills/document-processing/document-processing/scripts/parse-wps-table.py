#!/usr/bin/env python3
"""
解析 WPS/Excel 表格（含合并单元格）→ JSON。
用法：python parse-wps-table.py <输入.et/.xls/.xlsx> [输出.json]
"""
import json, re, sys, subprocess

def parse_wps_table(input_path, output_path=None):
    # 1. MarkItDown 提取
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", input_path],
        capture_output=True, text=True, timeout=30
    )
    text = result.stdout

    # 2. 解析表格行
    rows = []
    for line in text.split('\n'):
        if not line.startswith('| '):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if '一级指标' in line:
            continue
        if all(c.replace('-','').strip() == '' for c in cells):
            continue
        clean = []
        for c in cells:
            if c in ('NaN', '', 'Unnamed', '/') or c.startswith('Unnamed'):
                clean.append(None)
            else:
                clean.append(c)
        rows.append(clean)

    # 3. 重建合并单元格层级
    l1 = l2 = l3 = None
    parsed = []
    for row in rows:
        if row[0] and row[0] != '小计':
            l1 = row[0]; l2 = None; l3 = None
        elif row[0] == '小计':
            continue
        if row[1]: l2 = row[1]
        if row[2]: l3 = row[2]
        criteria = row[3] if len(row) > 3 else None
        score = row[4] if len(row) > 4 else None
        note = row[7] if len(row) > 7 else None
        if criteria:
            parsed.append(dict(L1=l1, L2=l2, L3=l3, criteria=criteria, score=score, note=note))

    # 4. 建树
    def build(items):
        tree = []
        l1_order = list(dict.fromkeys(it['L1'] for it in items if it['L1']))
        for l1_name in l1_order:
            wm = re.search(r'[（(]([\d.]+)[）)]', l1_name or '')
            weight = float(wm.group(1)) if wm else None
            clean = re.sub(r'\s*[（(][\d.]+[）)]\s*', '', l1_name).strip()
            node = dict(name=clean, weight=weight, children=[])
            l2_items = [it for it in items if it['L1'] == l1_name]
            l2_order = list(dict.fromkeys(it['L2'] for it in l2_items if it['L2']))
            for l2_name in l2_order:
                l2_node = dict(name=l2_name, children=[])
                l3_items = [it for it in l2_items if it['L2'] == l2_name]
                l3_order = list(dict.fromkeys(it['L3'] for it in l3_items if it['L3']))
                for l3_name in l3_order:
                    entries = [dict(content=it['criteria'])
                               for it in l3_items if it['L3'] == l3_name and it['criteria']]
                    for it in l3_items:
                        if it['L3'] == l3_name and it['criteria']:
                            entry = dict(content=it['criteria'])
                            if it['score']: entry['score'] = it['score']
                            if it['note']: entry['note'] = it['note']
                            entries.append(entry)
                    # 去重用
                    seen = set()
                    unique = []
                    for e in entries:
                        if e['content'] not in seen:
                            seen.add(e['content'])
                            unique.append(e)
                    l2_node['children'].append(dict(name=l3_name, criteria=unique))
                node['children'].append(l2_node)
            tree.append(node)
        return tree

    tree = build(parsed)
    output = json.dumps(tree, ensure_ascii=False, indent=2)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已输出: {output_path}")

    return output

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: parse-wps-table.py <输入文件> [输出.json]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    parse_wps_table(inp, out)