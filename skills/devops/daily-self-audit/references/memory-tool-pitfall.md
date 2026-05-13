# memory 工具操作陷阱

## 问题

`memory` 工具的 `remove` 和 `replace` 动作使用 `old_text` **子串匹配**来定位条目，而非精确匹配。

```
memory action=remove target=memory old_text="短文本"
```

如果 `old_text` 是某个条目的子串，可能误删多个条目。

## 实测案例

```
memory action=remove target=memory old_text="test"
```

返回：
```
error: "Multiple entries matched 'test'. Be more specific."
```

更危险的是，如果子串恰好唯一匹配到某个条目，会直接删除该条目——**没有二次确认**。

## 正确做法

| 场景 | 推荐方法 |
|------|----------|
| 单条精确修改 | `memory action=replace` + 足够长的`old_text`（包含唯一标识） |
| 批量操作/全量重写 | **禁止用 memory 工具** → 用 `write_file` 直接覆盖 `~/.hermes/memories/MEMORY.md` |
| 删除单条 | `memory action=remove` + 完整条目文本（非子串） |

## 安全流程

1. **先备份**：`cp ~/.hermes/memories/MEMORY.md ~/.hermes/memories/MEMORY.md.bak`
2. **批量操作**：用 `write_file` 写入完整内容（覆盖整个文件）
3. **单条修改**：用 `memory action=replace`，`old_text` 至少包含条目完整内容
4. **验证**：操作后 `cat ~/.hermes/memories/MEMORY.md` 确认结果

## 记忆

memory 工具本身记录在 `~/.hermes/memories/MEMORY.md` 中，但工具操作的是内存中的条目列表，与文件内容可能不同步。写文件后需用 `memory` 工具重新读取确认。