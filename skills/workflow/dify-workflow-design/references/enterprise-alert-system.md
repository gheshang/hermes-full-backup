# Dify 工作流：企业告警系统设计模式

## 核心架构

```
信息接收层 → 分析层 (Dify) → 告警层
    │              │              │
  飞书/企微    混合规则+LLM    飞书卡片
```

## 混合规则设计模式

### Step 1: 固定规则节点（优先级最高）
```
条件判断节点配置：
IF query CONTAINS "紧急" OR "故障" OR "报警" OR "宕机"
   OR query CONTAINS "CPU>90%" OR "内存>95%"
   OR query CONTAINS "安全" AND ("入侵" OR "泄露")
THEN rule_alert = true
ELSE rule_alert = false
```

### Step 2: LLM 分析节点（规则未命中时）
```
Prompt 模板：
"""
分析以下消息的告警等级：
消息：{{query}}

输出JSON（严格格式）：
{
  "alert_level": "high|medium|low|normal",
  "summary": "简短摘要（20字内）",
  "conclusion": "AI分析结论和建议",
  "keywords": ["关键词1", "关键词2"],
  "suggested_action": "建议操作"
}

告警等级标准：
- high: 系统故障、数据丢失、安全事件、紧急故障
- medium: 性能下降、异常波动、需要关注
- low: 一般提醒、信息通知
- normal: 无需告警，正常信息
"""
```

### Step 3: 混合决策逻辑
```
IF rule_alert == true → 直接 high（跳过 LLM，快速响应）
ELSE → 使用 LLM 输出
```

## 飞书卡片推送模板

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "🚨 {{alert_level}} 告警"},
      "template": "red|blue"
    },
    "elements": [
      {"tag": "div", "text": {"tag": "lark_md", "content": "**摘要：**{{summary}}"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "**AI分析结论：**{{conclusion}}"}},
      {"tag": "action", "actions": [
        {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"}, "type": "primary", "url": "{{link}}"}
      ]}
    ]
  }
}
```

## 避坑清单

| 坑 | 现象 | 解决方案 |
|----|------|----------|
| 飞书签名验证失败 | 403错误 | 必须实现 gen_sign 函数，时间戳用当前时间 |
| Dify 工作流超时 | 分析慢/失败 | 设置 response_mode: blocking，超时60s+ |
| 告警风暴 | 频繁告警轰炸 | 添加去重逻辑：5分钟内相同内容只发一次 |
| LLM误判 | 普通消息被标为告警 | Prompt中明确"正常消息不要告警"，加few-shot示例 |
| 混合规则冲突 | 规则+LLM结果不一致 | 规则优先级高于LLM，LLM只做补充判断 |

## 3天MVP 执行计划

### Day 1: 飞书接入 + 固定规则告警
- 飞书开发者后台创建应用
- FastAPI 统一接入服务（接收飞书/企微 Webhook）
- Dify 简单工作流（关键词匹配）
- 飞书卡片推送测试

### Day 2: Dify 混合规则工作流 + LLM 分析
- Dify 条件判断节点（固定规则）
- Dify LLM 分析节点（上下文理解）
- HTTP 请求节点（调用飞书 Webhook）
- 混合决策逻辑

### Day 3: 企业微信接入 + 联调测试
- 企业微信自建应用配置
- Flask 接收服务部署
- 双通道联调测试

## 环境变量配置

```bash
# 飞书
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=*** 企业微信
WECHAT_CORP_ID=wwxxx
WECHAT_AGENT_ID=1000001
WECHAT_SECRET=***
W...n
# Dify
DIFY_API_URL=https://api.dify.ai/v1
DIFY_API_KEY=***
D...n
# 服务器
SERVER_PUBLIC_IP=你的服务器公网IP
```

## 相关技能

- `dify-workflow-design`: Dify 工作流设计通用方法论
- `grill-me`: 需求澄清（执行前必用）
- `native-mcp`: MCP 集成（可选扩展）