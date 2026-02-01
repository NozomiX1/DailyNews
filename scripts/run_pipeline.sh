#!/bin/bash
# 手动运行完整流程

set -e

# 获取脚本所在目录的父目录（项目根目录）
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 进入项目目录
cd "$PROJECT_DIR"

# 解析参数
DATE_ARG=""
DRY_RUN=""
FETCH_ONLY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --date)
            DATE_ARG="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --fetch-only)
            FETCH_ONLY="--fetch-only"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --date DATE      指定日期 (YYYY-MM-DD)，默认昨天"
            echo "  --dry-run        只运行到格式化，不发布"
            echo "  --fetch-only     只爬取数据"
            echo "  -h, --help       显示帮助"
            echo ""
            echo "Examples:"
            echo "  $0                    # 运行完整流程（昨天）"
            echo "  $0 --date 2026-02-01  # 运行指定日期"
            echo "  $0 --dry-run          # 只生成不发布"
            exit 0
            ;;
        *)
            # 位置参数作为日期
            if [[ -z "$DATE_ARG" ]]; then
                DATE_ARG="$1"
            fi
            shift
            ;;
    esac
done

# 构建命令
CMD="python main.py"
if [[ -n "$DATE_ARG" ]]; then
    CMD="$CMD $DATE_ARG"
fi
if [[ -n "$DRY_RUN" ]]; then
    CMD="$CMD $DRY_RUN"
fi
if [[ -n "$FETCH_ONLY" ]]; then
    CMD="$CMD $FETCH_ONLY"
fi

echo "========================================"
echo "  DailyNews Pipeline"
echo "========================================"
echo "项目目录: $PROJECT_DIR"
echo "执行命令: $CMD"
echo "========================================"
echo ""

# 执行
eval $CMD
