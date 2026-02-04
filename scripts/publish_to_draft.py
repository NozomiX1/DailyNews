#!/usr/bin/env python3
"""
将指定日期的所有内容推送到微信公众号草稿箱

Usage:
    python scripts/publish_to_draft.py --date 2026-01-31
    python scripts/publish_to_draft.py  # 默认昨天
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.publishers.wechat import WechatPublisher


def publish_date(date_str: str):
    """
    发布指定日期的所有内容到微信公众号草稿箱

    Args:
        date_str: 日期字符串 (YYYY-MM-DD)

    Returns:
        结果统计字典
    """
    publisher = WechatPublisher()
    output_dir = project_root / "output" / date_str

    if not output_dir.exists():
        print(f"❌ 目录不存在: {output_dir}")
        return {
            'success': 0,
            'failed': 0,
            'results': []
        }

    results = []
    success_count = 0
    failed_count = 0

    print(f"\n{'='*60}")
    print(f"开始发布 {date_str} 的内容")
    print(f"{'='*60}\n")

    # 1. 发布每日情报
    daily_report_path = output_dir / "daily_report.md"
    if daily_report_path.exists():
        print(f"[1/4] 发布 AI 每日情报...")
        try:
            result = publisher.publish_daily_report(
                str(daily_report_path),
                target_date=date_str
            )
            results.append({
                'type': 'AI 每日情报',
                'status': 'success',
                'draft_id': result.get('draft_id'),
                'count': result.get('count')
            })
            success_count += 1
            print(f"  ✅ 成功 - draft_id: {result.get('draft_id')}, 文章数: {result.get('count')}")
        except Exception as e:
            results.append({
                'type': 'AI 每日情报',
                'status': 'failed',
                'error': str(e)
            })
            failed_count += 1
            print(f"  ❌ 失败 - {e}")
    else:
        print(f"[1/4] ⏭️  AI 每日情报文件不存在，跳过")

    # 2. 发布 GitHub Trending
    trending_path = output_dir / "github_trending.md"
    if trending_path.exists():
        print(f"\n[2/4] 发布 GitHub 热门项目...")
        try:
            result = publisher.publish_github_trending(str(trending_path))
            results.append({
                'type': 'GitHub Trending',
                'status': 'success',
                'draft_id': result.get('draft_id'),
                'count': result.get('count')
            })
            success_count += 1
            print(f"  ✅ 成功 - draft_id: {result.get('draft_id')}, 项目数: {result.get('count')}")
        except Exception as e:
            results.append({
                'type': 'GitHub Trending',
                'status': 'failed',
                'error': str(e)
            })
            failed_count += 1
            print(f"  ❌ 失败 - {e}")
    else:
        print(f"\n[2/4] ⏭️  GitHub Trending 文件不存在，跳过")

    # 3. 发布论文汇总
    papers_summary_path = output_dir / "papers" / "papers_summary.md"
    if papers_summary_path.exists():
        print(f"\n[3/4] 发布每日论文汇总...")
        try:
            result = publisher.publish_papers_summary(str(papers_summary_path))
            results.append({
                'type': '论文汇总',
                'status': 'success',
                'draft_id': result.get('draft_id'),
                'count': result.get('count')
            })
            success_count += 1
            print(f"  ✅ 成功 - draft_id: {result.get('draft_id')}, 论文数: {result.get('count')}")
        except Exception as e:
            results.append({
                'type': '论文汇总',
                'status': 'failed',
                'error': str(e)
            })
            failed_count += 1
            print(f"  ❌ 失败 - {e}")
    else:
        print(f"\n[3/4] ⏭️  论文汇总文件不存在，跳过")

    # 4. 发布单篇论文分析
    papers_dir = output_dir / "papers"
    if papers_dir.exists() and papers_dir.is_dir():
        paper_files = [f for f in papers_dir.glob("*.md") if f.name != "papers_summary.md"]
        if paper_files:
            print(f"\n[4/4] 发布单篇论文分析...")
            print(f"  找到 {len(paper_files)} 篇论文分析")
            for i, paper_file in enumerate(paper_files, 1):
                print(f"  [{i}/{len(paper_files)}] {paper_file.stem}")
                try:
                    result = publisher.publish_single_paper(str(paper_file))
                    results.append({
                        'type': f'论文分析: {paper_file.stem}',
                        'status': 'success',
                        'draft_id': result.get('draft_id')
                    })
                    success_count += 1
                    print(f"    ✅ 成功 - draft_id: {result.get('draft_id')}")
                except Exception as e:
                    results.append({
                        'type': f'论文分析: {paper_file.stem}',
                        'status': 'failed',
                        'error': str(e)
                    })
                    failed_count += 1
                    print(f"    ❌ 失败 - {e}")
        else:
            print(f"\n[4/4] ⏭️  没有找到论文分析文件")
    else:
        print(f"\n[4/4] ⏭️  论文目录不存在，跳过")

    # 汇总统计
    print(f"\n{'='*60}")
    print(f"发布完成 - {date_str}")
    print(f"{'='*60}")
    print(f"成功: {success_count} | 失败: {failed_count} | 总计: {len(results)}")

    return {
        'success': success_count,
        'failed': failed_count,
        'results': results
    }


def main():
    parser = argparse.ArgumentParser(
        description='推送指定日期的内容到微信公众号草稿箱'
    )
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='日期 (YYYY-MM-DD)，默认为昨天'
    )

    args = parser.parse_args()

    # 默认使用昨天的日期
    if args.date is None:
        yesterday = datetime.now() - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")
    else:
        target_date = args.date

    # 验证日期格式
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"❌ 无效的日期格式: {target_date}，请使用 YYYY-MM-DD 格式")
        sys.exit(1)

    publish_date(target_date)


if __name__ == "__main__":
    main()
