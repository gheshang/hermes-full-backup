# WPS Office .doc 文本提取指南

## 问题

WPS Office 生成的 `.doc` 文件（旧格式，非 `.docx`）无法被 pandoc 或 python-docx 读取，因为它是 OLE2 容器格式。

## 解决方案

```python
import olefile
import struct

doc_path = "path/to/file.doc"
ole = olefile.OleFileIO(doc_path)

# 读取 WordDocument 流
wd = ole.openstream('WordDocument').read()

text = []
i = 0
while i < len(wd) - 1:
    char = struct.unpack_from('<H', wd, i)[0]
    # CJK Unified Ideographs (4E00-9FFF)
    # CJK Symbols/Punctuation (3000-303F)
    # Fullwidth Forms (FF00-FFEF)
    # ASCII printable (0020-007E)
    if 0x4e00 <= char <= 0x9fff or 0x3000 <= char <= 0x303f or 0xff00 <= char <= 0xffef:
        text.append(chr(char))
    elif char == 0x000d:
        text.append('\n')
    elif 0x0020 <= char <= 0x007e:
        text.append(chr(char))
    elif char in (0x0009, 0x000a):
        text.append('\n')
    i += 2

ole.close()
result = ''.join(text)
```

## 清理步骤（必做）

1. **截断末尾垃圾**：正文末尾有大量 OLE 二进制残留（CJK B/C/D/E 扩展区乱码+控制字符），用 `head -N` 截断到最后一个有效行
   ```bash
   head -394 extracted.txt > clean.txt  # N=最后一个有效行号
   ```

2. **清理首行前缀**：首行可能有 OLE 控制字符前缀（如 `袉倔卋卋$2(#`），用 sed 删除：
   ```bash
   sed -i '1s/^[^锁]*//' clean.txt  # 替换"锁"为第一个有效字符
   ```

3. **验证**：`wc -c` 确认文件大小在合理范围（~20-30KB 对 8000 词的小说，中文约 2-3 字节/字）

## 飞书文件陷阱

飞书接收的 .doc 文件可能在 `~/novel/` 下为空（0 bytes），实际内容位于：
```
/home/hangskf/.hermes/cache/documents/doc_<hash>_<filename>.doc
```
使用 `file` 命令确认哪个是有效文件。
