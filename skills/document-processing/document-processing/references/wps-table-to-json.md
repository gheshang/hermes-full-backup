# WPS / Excel 表格 → JSON：合并单元格层级重建

> 适用场景：政府机关/国企的评分表、审计表、报表等，表格有大量合并单元格（行/列合并），需要保留多层级的父子关系（一级指标→二级指标→三级指标→评分标准）。

## 问题

WPS `.et` 文件或 Excel `.xls`/`.xlsx` 文件转 Markdown 后，合并单元格表现为：
- 下级行留空（`NaN` 或 `Unnamed`）
- 层级信息丢失——不能直接看出哪个二级指标属于哪个一级指标

## 方案

两步走：**MarkItDown 提取** → **Python 重建层级**

### 1. MarkItDown 提取

```bash
pip install 'markitdown[all]'
markitdown 评分标准.et
```

输出示例（表格 Markdown）：
```
| 一级指标 | 二级指标 | 三级指标 | 评分标准 | 分值 | ... |
| 经济政策执行权（0.30） | 经济政策执行 | 贯彻落实中央... | 1.未落实... | 15 | ... |
| NaN | NaN | NaN | 2.违反... | NaN | ... |
```

### 2. Python 层级重建

核心逻辑（伪代码）：

```python
# 第一步：解析 MarkItDown 输出的表格行
rows = parse_markdown_table(text)

# 第二步：跟踪合并单元格
level1 = None
level2 = None
level3 = None
parsed = []

for row in rows:
    if row[0] and row[0] != '小计':
        level1 = row[0]      # 新的 L1 出现，重置 L2/L3
        level2 = None
        level3 = None
    if row[1]:
        level2 = row[1]      # 新的 L2
    if row[2]:
        level3 = row[2]      # 新的 L3
    # 只保留有评分标准的行
    if row[3]:               # 评分标准列
        parsed.append({
            'L1': level1, 'L2': level2, 'L3': level3,
            'criteria': row[3], 'score': row[4], 'note': row[7]
        })

# 第三步：建树（L1 → L2 → L3 → criteria[]）
tree = build_nested_tree(parsed)
# 输出：一级指标按出现顺序，每个含二级指标列表
# 每个二级指标含三级指标列表，每个三级指标含评分标准列表
```

### 3. 完整示例脚本

见同一 Skill 下的 `scripts/parse-wps-table.py`。

## 关键点

| 问题 | 解决方案 |
|------|---------|
| 合并单元格留空 | 用上一个非空值填充（Forward-fill） |
| 权重提取 | 从 L1 名称中用正则提取 `（0.30）` → `0.3` |
| 小计行 | 跳过（不计入数据） |
| 加分项 | 当独立的一级指标处理 |
| 保持顺序 | 用 List 而非 Dict 保证 JSON 输出顺序与表格一致 |

## 正则备忘

```python
# 提取权重
import re
weight = re.search(r'[（(]([\d.]+)[）)]', '经济政策执行权（0.30）')
# → 0.3

# 清干净名称
clean_name = re.sub(r'\s*[（(][\d.]+[）)]\s*', '', l1_name).strip()
# → "经济政策执行权"

# 检测小计行
is_total = (row[0] == '小计')  # 跳过