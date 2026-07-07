# 连州招聘信息每日爬取 — 脚本参考

## 项目概述

每日自动爬取广东清远连州地区的公务员和教师招聘信息，特别关注舞蹈/艺术/体艺相关岗位。

## 脚本位置

```
~/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/lianzhou-jobs-crawler.py
```

## 监控源（4个站点）

| 站点 | URL | 类型 |
|------|-----|------|
| 连州市公务员招考 | `lianzhou.gov.cn/xxgk/rsxx/gwyzk/` | 公务员 |
| 连州市事业单位招聘 | `lianzhou.gov.cn/xxgk/rsxx/sydwzp/` | 事业单位/教师 |
| 清远教师招聘网 | `jrzhufu.com/news/news_81.html` | 教师（清远全域） |
| 清远事业单位招聘汇总 | `yingyudengji.com/news/news_81.html` | 事业单位（清远全域） |

## 舞蹈关键词覆盖

`舞蹈、舞、艺术、文艺、表演、音乐、美术、体育、体艺、音体美、特长生、艺术团、舞蹈教师、舞蹈老师、艺术教师、艺术岗、文化站、文化馆、少年宫`

## 使用方法

```bash
# 直接运行
python3 ~/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/lianzhou-jobs-crawler.py

# 配合 cron 每日定时（推荐上午8点）
0 8 * * * cd /home/hangskf && python3 ~/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/lianzhou-jobs-crawler.py >> ~/.hermes/cron/lian-zhou-jobs/cron.log 2>&1
```

## 输出

- **报告文件**：`~/.hermes/cron/lian-zhou-jobs/YYYY-MM-DD.md`
- **历史记录**：`~/.hermes/cron/lian-zhou-jobs/history.json`（保留90天，去重）

## 注意事项

1. **crontab 安装方式**：不要用 `(crontab -l; echo "...") | crontab -`（可能挂起），改用：
   ```bash
   echo "0 8 * * * ..." > /tmp/crontab.txt
   crontab /tmp/crontab.txt
   crontab -l  # 验证
   ```

2. **舞蹈岗位季节性**：连州教师招聘通常集中在每年 3-5 月（赴高校设点招聘）和 7-8 月（事业单位集中招聘），其他时间舞蹈岗位较少。

3. **依赖**：优先使用 `requests` 库，无则降级为 `urllib`。
