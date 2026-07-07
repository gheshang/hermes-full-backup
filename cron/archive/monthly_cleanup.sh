#!/bin/bash
DAYS=${1:-90}
echo "=== 清理超过 $DAYS 天的存档 ==="
for job_dir in /home/hangskf/.hermes/cron/output/*; do
    [ -d "$job_dir" ] || continue
    find "$job_dir" -name "*.md" -mtime +$DAYS -delete 2>/dev/null
    COUNT=$(ls "$job_dir"/*.md 2>/dev/null | wc -l)
    echo "  $(basename $job_dir): 保留 $COUNT 个文件"
done
find /home/hangskf/.hermes/cron/lian-zhou-jobs -name "*.md" -mtime +$DAYS -delete 2>/dev/null
find /home/hangskf/.hermes/cron/lian-zhou-jobs -name "*.log" -mtime +$DAYS -delete 2>/dev/null
echo "  lian-zhou-jobs: 已清理"
echo "=== 完成 ==="
