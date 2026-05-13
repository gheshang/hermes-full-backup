# Edge TTS 中文语音合成

使用 Microsoft Edge TTS 进行免费中文语音合成，无需 API Key。

## 基本信息

| 项目 | 值 |
|------|-----|
| **引擎** | Microsoft Edge TTS（免费） |
| **安装** | `pip install edge-tts` |
| **限制** | 无 API Key 限制，但需遵守微软服务条款 |

## 可用中文语音

| 语音名 | 性别 | 风格 | 适用场景 |
|--------|------|------|----------|
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖、新闻、小说 | 通用推荐 |
| `zh-CN-XiaoyiNeural` | 女 | 活泼、卡通 | 儿童内容 |
| `zh-CN-YunjianNeural` | 男 | 激情、体育、小说 | 运动/激情内容 |
| `zh-CN-YunxiNeural` | 男 | 阳光、小说 | 通用男声 |
| `zh-CN-YunxiaNeural` | 男 | 可爱、卡通 | 儿童内容 |
| `zh-CN-YunyangNeural` | 男 | 专业、新闻 | 正式内容 |
| `zh-CN-liaoning-XiaobeiNeural` | 女 | 幽默、方言 | 东北方言 |
| `zh-CN-shaanxi-XiaoniNeural` | 女 | 明亮、方言 | 陕西方言 |

## 命令行使用

```bash
# 基本使用
edge-tts --voice "zh-CN-XiaoxiaoNeural" --text "你好，这是测试语音。" --write-media output.mp3

# 从文件读取文本
edge-tts --voice "zh-CN-XiaoxiaoNeural" --file input.txt --write-media output.mp3

# 列出所有可用语音
edge-tts --list-voices

# 筛选中文语音
edge-tts --list-voices | grep "zh-CN"
```

## Python 使用

```python
import asyncio
import edge_tts

async def generate_speech(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

# 使用
asyncio.run(generate_speech("你好，这是测试语音。", "output.mp3"))
```

## 配置到 config.yaml

```yaml
tts:
  provider: edge
  edge:
    voice: zh-CN-XiaoxiaoNeural
```

## 注意事项

1. **网络要求**：需要能访问微软 Edge TTS 服务
2. **文件大小**：生成的 MP3 文件通常较小（80KB/10秒左右）
3. **并发限制**：建议避免高频并发调用
4. **中文支持**：所有 `zh-CN-*` 语音都支持中文，无需额外配置

## 常见问题

### 问题：中文发音不自然
**解决**：尝试更换语音，`XiaoxiaoNeural` 和 `YunyangNeural` 通常最自然。

### 问题：标点符号影响节奏
**解决**：适当调整标点，或使用 SSML 标签控制语速和停顿。

### 问题：长文本生成失败
**解决**：将长文本分段生成，每段不超过 500 字。
