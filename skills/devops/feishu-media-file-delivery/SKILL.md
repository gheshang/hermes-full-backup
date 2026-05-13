---
name: feishu-media-file-delivery
description: 飞书文件附件发送的修补方案——Hermes send_message 工具层拦截了飞书 MEDIA 分发，需要改两处代码才能让飞书支持文件附件发送。
version: 1.0
author: 上河一号
metadata:
  hermes:
    tags: [feishu, media, file, send_message, patch]
---

# 飞书文件附件发送修补方案

## 问题

飞书对话里用 `send_message` 发 `MEDIA:/path/to/file` 时，文件附件被静默丢弃，只发出文本。

原因：`send_message_tool.py` 在工具层做了白名单拦截，飞书不在白名单里。

## 根因分析

飞书适配器 **底层完全支持** 文件上传和发送：

- `feishu.py:1834` — `send_document()` 走 `_send_uploaded_file_message`
- `feishu.py:1815` — `send_voice()` 走 `_send_uploaded_file_message`
- `feishu.py:1854` — `send_video()` 走 `_send_uploaded_file_message`
- `feishu.py:1873` — `send_image_file()` 走图片上传 API
- `feishu.py:1391` — `_send_feishu()` 函数已有完整的 media 分发逻辑（按扩展名分流到 send_image_file/send_video/send_voice/send_document）

**但工具层拦截了飞书**：

1. **白名单拦截**（`send_message_tool.py:531-544`）—— `_MEDIA_PLATFORMS` 白名单只有 telegram/discord/matrix/weixin/signal，feishu 不在列，media_files 被打 warning 后跳过
2. **参数缺失**（`send_message_tool.py:570`）—— `_send_feishu` 调用时没传 `media_files` 参数

## 修补方案（两处改动）

### 改动1：白名单加入 feishu

文件：`~/.hermes/hermes-agent/tools/send_message_tool.py`

将第531-544行的无条件拦截改为条件拦截：

```python
# --- Non-media platforms ---
_MEDIA_PLATFORMS = {"telegram", "discord", "matrix", "weixin", "signal", "feishu"}
if media_files and not message.strip():
    if platform.value not in _MEDIA_PLATFORMS:
        return {
            "error": (
                f"send_message MEDIA delivery is currently only supported for telegram, discord, matrix, weixin, signal, and feishu; "
                f"target {platform.value} had only media attachments"
            )
        }
warning = None
if media_files:
    if platform.value not in _MEDIA_PLATFORMS:
        warning = (
            f"MEDIA attachments were omitted for {platform.value}; "
            "native send_message media delivery is currently only supported for telegram, discord, matrix, weixin, signal, and feishu"
        )
```

### 改动2：_send_feishu 传入 media_files

同一文件，第570行：

```python
# 原：result = await _send_feishu(pconfig, chat_id, chunk, thread_id=thread_id)
# 改：需要 is_last 判断，媒体只随最后一条文本消息发送

# 同时需要把循环从 for chunk in chunks 改为 for i, chunk in enumerate(chunks)：
for i, chunk in enumerate(chunks):
    is_last = (i == len(chunks) - 1)
    ...
    elif platform == Platform.FEISHU:
        result = await _send_feishu(pconfig, chat_id, chunk, media_files=media_files if is_last else [], thread_id=thread_id)
```

## 验证

修补后重启 gateway，发送 `MEDIA:/path/to/file.md` 到飞书，应收到文件附件。

## 注意

- 修补后需重启 gateway 才能生效（gateway 进程会缓存旧代码）
- 改的是 Hermes 源码，`hermes update` 后会被覆盖，需重新打补丁
- 图片发送（`send_image_file`）走单独路径，不受此限制——飞书一直支持图片
