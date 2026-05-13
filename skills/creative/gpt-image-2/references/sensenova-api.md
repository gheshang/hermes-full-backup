# SenseNova 图像生成 API

商汤科技 SenseNova 图像生成服务，兼容 OpenAI `/v1/images/generations` 格式。

## 基本信息

| 项目 | 值 |
|------|-----|
| **Base URL** | `https://token.sensenova.cn/v1` |
| **图像生成端点** | `POST /v1/images/generations` |
| **模型 ID** | `sensenova-u1-fast` |
| **鉴权** | `Authorization: Bearer {api_key}` |
| **调用限制** | 每5小时1500次 |

## 支持的尺寸

⚠️ **重要**：SenseNova U1 Fast 不支持 OpenAI 的标准尺寸（1024x1024 等），必须使用以下尺寸之一：

| 尺寸 | 用途 |
|------|------|
| `1664x2496` | 竖版海报 |
| `2496x1664` | 横版海报 |
| `1760x2368` | 竖版 |
| `2368x1760` | 横版 |
| `1824x2272` | 竖版 |
| `2272x1824` | 横版 |
| `2048x2048` | 正方形 |
| `2752x1536` | 宽屏横版 |
| `1536x2752` | 宽屏竖版 |
| `3072x1376` | 超宽横版 |
| `1344x3136` | 超宽竖版（推荐竖版构图） |

## 请求格式

```json
{
  "model": "sensenova-u1-fast",
  "prompt": "Chinese ink wash painting, a graceful female dancer...",
  "n": 1,
  "size": "1344x3136",
  "response_format": "b64_json"
}
```

## 响应格式

```json
{
  "data": [{
    "b64_json": "base64_encoded_image_data",
    "url": "https://..."  // 可选，签名URL有时效性
  }]
}
```

## 配置到 config.yaml

```yaml
model:
  image:
    model: sensenova-u1-fast
    base_url: https://token.sensenova.cn/v1/images/generations
    api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## cURL 示例

```bash
curl https://token.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer sk-xxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sensenova-u1-fast",
    "prompt": "你的提示词",
    "n": 1,
    "size": "1344x3136",
    "response_format": "b64_json"
  }'
```

## 注意事项

1. **尺寸限制**：必须使用支持的尺寸，否则会返回 `field Size invalid` 错误
2. **签名URL时效**：返回的 `url` 字段有时效性（通常1小时），建议优先使用 `b64_json`
3. **响应格式**：默认返回 `url`，设置 `response_format: "b64_json"` 可获取 base64 数据
4. **中文提示词**：支持中文提示词，但英文通常效果更好

## 文档链接

- 官方文档：https://platform.sensenova.cn/docs
- 控制台：https://platform.sensenova.cn/console/keys
