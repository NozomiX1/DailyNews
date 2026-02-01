#!/bin/bash
# 安装 DailyNews 定时任务

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 检查是否已安装
if crontab -l 2>/dev/null | grep -q "DailyNews/main.py"; then
    echo "⚠️ 检测到已存在的 DailyNews cron 任务"
    echo "是否要覆盖？(y/n)"
    read -r answer
    if [ "$answer" != "y" ]; then
        echo "取消安装"
        exit 0
    fi
    # 删除旧任务
    crontab -l 2>/dev/null | grep -v "DailyNews/main.py" | crontab -
fi

# 添加 cron 任务（每天晚上 11 点运行）
# 0 23 * * * 表示每天 23:00
(crontab -l 2>/dev/null; echo "0 23 * * * cd $PROJECT_DIR && python main.py >> $LOG_DIR/pipeline_\$(date +\%Y\%m\%d).log 2>&1") | crontab -

echo "✅ Cron 任务已安装!"
echo ""
echo "📋 当前 crontab:"
crontab -l | grep -E "(DailyNews|23 \* \* \*)"
echo ""
echo "📁 日志目录: $LOG_DIR"
echo ""
echo "查看日志:"
echo "  tail -f $LOG_DIR/pipeline_\$(date +%Y%m%d).log"
echo ""
echo "手动运行:"
echo "  cd $PROJECT_DIR && python main.py"
