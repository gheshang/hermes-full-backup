#!/bin/bash
DATE=${1:-$(date +%Y-%m-%d)}
OUTPUT_DIR="/home/hangskf/.hermes/cron/output"
LIAN_ZOU_DIR="/home/hangskf/.hermes/cron/lian-zhou-jobs"

echo "# 定时任务每日汇总: $DATE"
echo ""
echo "## Hermes Cron 任务"
for job_dir in "$OUTPUT_DIR"/*; do
    [ -d "$job_dir" ] || continue
    JOB_ID=$(basename "$job_dir")
    FILE=$(ls "$job_dir"/*"$DATE"* 2>/dev/null | head -1)
    if [ -n "$FILE" ]; then
        LINES=$(wc -l < "$FILE")
        echo "- **$JOB_ID**: $LINES 行"
    else
        echo "- **$JOB_ID**: 无输出"
    fi
done
echo ""
echo "## 系统 Crontab"
if [ -f "$LIAN_ZOU_DIR/$DATE.md" ]; then
    LINES=$(wc -l < "$LIAN_ZOU_DIR/$DATE.md")
    echo "- lian-zhou-jobs: $LINES 行"
else
    echo "- lian-zhou-jobs: 无输出"
fi
