# Feishu MEDIA 协议限制

飞书（Lark）平台对 MEDIA 类型消息的支持限制。

## 现状

| 平台 | MEDIA 支持 | 语音气泡 |
|------|-----------|---------|
| Telegram | ✅ | 支持 |
| Discord | ✅ | 支持 |
| 微信 | ✅ | 支持 |
| **飞书** | ❌ | **不支持** |
| Signal | ✅ | 支持 |
| Matrix | ✅ | 支持 |

## 错误信息

```
send_message MEDIA delivery is currently only supported for telegram, discord, 
matrix, weixin, signal and yuanbao; target feishu had only media attachments
```

## 解决方案

### 方案 1：文件附件
飞书支持将媒体文件作为普通附件发送，但不会显示为语音气泡。

```python
# 在 Hermes 中
send_message(
    message="🎙️ 语音文件：xxx.mp3",
    target="feishu"
)
# 文件需要单独通过飞书 API 上传
```

### 方案 2：上传到飞书云文档
将文件上传到飞书云文档，发送文档链接。

### 方案 3：换平台
使用支持 MEDIA 协议的平台（微信/Telegram/Discord）接收语音气泡。

## 临时规避

如果需要在飞书发送语音：

1. 生成语音文件到 `~/.hermes/audio_cache/`
2. 通过飞书机器人 API 上传文件
3. 发送文件消息

```bash
# 使用飞书 API 上传文件
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources" \
  -H "Authorization: Bearer {app_access_token}" \
  -F "file_type=audio" \
  -F "file=@/path/to/audio.mp3"
```

## 建议

- 如果主要使用飞书通信，建议将 TTS 功能改为生成文件并提供下载链接
- 或在 config.yaml 中配置多平台，优先使用支持 MEDIA 的平台发送语音
