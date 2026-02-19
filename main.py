#!/usr/bin/env python3
"""
DailyNews Main Entry Point

全自动运行入口：每天晚上11点通过 cron 调用，完成爬取、总结、发布全流程。

默认日期策略：
- 所有模块（公众号、GitHub Trending、论文）：今天
- 周末自动跳过论文爬取（arXiv 不发布）
- GitHub Trending 只能爬取当天数据

Usage:
    # 运行默认任务
    python main.py

    # 运行指定任务
    python main.py --wechat --github

    # 运行论文深度分析
    python main.py --analyze --paper-num 5

    # 运行指定日期的任务
    python main.py --date 2026-02-02 --wechat
"""
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.tasks import WechatArticleTask, GithubTrendingTask, PapersTask
from src.tasks.paper_analysis import PaperAnalysisTask
from src.summarizers import ZhipuClient
import config


def get_weekday(date_str: str) -> int:
    """获取星期几 (0=周一, 6=周日)"""
    return datetime.strptime(date_str, '%Y-%m-%d').weekday()


def is_weekend(date_str: str) -> bool:
    """判断是否是周末"""
    weekday = get_weekday(date_str)
    return weekday == 5 or weekday == 6  # 5=周六, 6=周日


def run_pipeline(date: str, tasks_to_run: list):
    """
    运行完整流程：爬取 → 总结 → 清理 → 格式化

    Args:
        date: 目标日期 (YYYY-MM-DD)
        tasks_to_run: 要运行的任务列表，包含 'wechat', 'github', 'paper'
    """
    today = datetime.now().strftime('%Y-%m-%d')

    # 判断星期几
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekday_idx = get_weekday(date)
    weekday_name = weekday_names[weekday_idx]

    # 判断是否跳过论文（周末）
    skip_papers = is_weekend(date)

    # 判断是否跳过 Trending（只能爬取当天）
    skip_trending = (date != today)

    print("=" * 60)
    print(f"🚀 DailyNews Pipeline - {date} ({weekday_name})")
    print("=" * 60)
    print(f"   公众号: {'✅' if 'wechat' in tasks_to_run else '❌'}")
    print(f"   Trending: {'✅' if 'github' in tasks_to_run else '❌'}")
    print(f"   论文轻量汇总: {'✅' if 'paper' in tasks_to_run else '❌'}")
    print(f"   输出目录: output/{date}/")
    print("=" * 60)

    # 初始化共享组件
    client = ZhipuClient(
        model=config.GLM_MODEL,
        api_key=config.GLM_API_KEY,
        base_url=config.GLM_BASE_URL,
        max_tokens=config.GLM_MAX_TOKENS,
        enable_thinking=config.GLM_ENABLE_THINKING,
    )
    output_dir = PROJECT_ROOT / "output" / date

    # 根据任务标志创建任务实例
    tasks = []
    if 'wechat' in tasks_to_run:
        tasks.append(WechatArticleTask(client=client, output_dir=output_dir))
    if 'github' in tasks_to_run and not skip_trending:
        tasks.append(GithubTrendingTask(client=client, output_dir=output_dir))
    if 'paper' in tasks_to_run and not skip_papers:
        tasks.append(PapersTask(client=client, output_dir=output_dir))

    # 执行所有任务
    results = {}
    for task in tasks:
        print(f"\n{'='*60}")
        print(f"📋 {task.name} - {date}")
        print(f"{'='*60}")

        result = task.run(date)
        results[task.name] = result

        # 打印结果
        task.print_result(result)

    # 汇总报告
    print("\n" + "=" * 60)
    print("✅ Pipeline Completed!")
    print("=" * 60)
    print(f"📁 输出目录: {output_dir}")

    # 打印错误
    for task_name, result in results.items():
        if result.get("errors"):
            print(f"\n⚠️ {task_name} 错误:")
            for error in result["errors"]:
                print(f"  - {error}")


def run_paper_analysis_pipeline(
    target_date: str = None,
    paper_num: int = 5
):
    """
    论文深度分析流程 - 获取、排序、下载、分析

    Args:
        target_date: 目标日期 (YYYY-MM-DD)，默认今天
        paper_num: 分析论文数量
    """
    # 默认今天
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print("=" * 80)
    print(f"Paper Analysis Pipeline - {target_date}")
    print("=" * 80)

    # 初始化组件
    client = ZhipuClient(
        model=config.GLM_MODEL,
        api_key=config.GLM_API_KEY,
        base_url=config.GLM_BASE_URL,
        max_tokens=config.GLM_MAX_TOKENS,
        enable_thinking=config.GLM_ENABLE_THINKING,
    )
    output_dir = PROJECT_ROOT / "output" / target_date

    # 创建任务实例
    task = PaperAnalysisTask(
        client=client,
        output_dir=output_dir,
        min_papers=paper_num,
        max_papers=paper_num,
        enable_topic_bonus=False
    )

    # 执行任务
    result = task.run(target_date)

    # 打印结果
    task.print_result(result)

    # 额外的汇总信息
    print("\n" + "=" * 80)
    print("Pipeline 完成!")
    print(f"  输出目录: {output_dir}")
    print(f"  分析数量: {result.get('summarized', 0)}")
    print("=" * 80)

    return result


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="DailyNews 全自动流程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 运行默认任务
  python main.py

  # 运行指定任务
  python main.py --wechat --github

  # 运行论文深度分析
  python main.py --analyze --paper-num 5

  # 运行指定日期的任务
  python main.py --date 2026-02-02 --wechat
        """
    )

    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='指定日期 (YYYY-MM-DD)，默认今天'
    )
    parser.add_argument(
        '--wechat',
        action='store_true',
        help='运行 WeChat 任务'
    )
    parser.add_argument(
        '--github',
        action='store_true',
        help='运行 GitHub Trending 任务'
    )
    parser.add_argument(
        '--paper',
        action='store_true',
        help='运行 Papers 轻量汇总任务'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='运行 Paper Analysis 深度分析任务'
    )
    parser.add_argument(
        '--paper-num',
        type=int,
        default=5,
        help='论文分析任务时的论文数量（仅在 --analyze 时有效，默认5）'
    )

    args = parser.parse_args()

    try:
        # 论文深度分析模式
        if args.analyze:
            run_paper_analysis_pipeline(
                target_date=args.date,
                paper_num=args.paper_num
            )
            return

        # 确定默认日期
        today = datetime.now().strftime('%Y-%m-%d')
        target_date = args.date if args.date else today

        # 确定要运行的任务
        tasks_to_run = []
        if args.wechat:
            tasks_to_run.append('wechat')
        if args.github:
            tasks_to_run.append('github')
        if args.paper:
            tasks_to_run.append('paper')

        # 如果没有指定任何任务标志，运行默认任务
        if not tasks_to_run:
            tasks_to_run.append('wechat')
            # Trending 只能爬取当天
            if target_date == today:
                tasks_to_run.append('github')
            # 论文周末不发布
            if not is_weekend(target_date):
                tasks_to_run.append('paper')

        # 主流程（爬取 → 总结 → 格式化）
        run_pipeline(date=target_date, tasks_to_run=tasks_to_run)

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
