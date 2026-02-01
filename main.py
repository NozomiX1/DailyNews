#!/usr/bin/env python3
"""
DailyNews Main Entry Point

全自动运行入口：每天晚上11点通过 cron 调用，完成爬取、总结、发布全流程。

默认日期策略：
- 公众号文章：今天
- GitHub Trending：今天
- HuggingFace 论文：昨天

Usage:
    python main.py [date]

    date: Optional date string in YYYY-MM-DD format
          当指定日期时：公众号和 GitHub 使用该日期，论文使用该日期的前一天
          （因为 HuggingFace 论文榜单只显示"昨天"的论文）
"""
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.fetchers import WechatFetcher, GithubTrendingFetcher, PapersFetcher
from src.summarizers import ArticleSummarizer, GithubSummarizer, PaperSummarizer, GeminiClient
from src.processors import LLMDeduplicator, MarkdownFormatter
from src.publishers import WechatPublisher
from src.utils.paper_ranker import PaperRanker
import config


def run_pipeline(date: str = None, dry_run: bool = False):
    """
    运行完整流程：爬取 → 总结 → 清理 → 格式化 → 发布

    Args:
        date: 目标日期 (YYYY-MM-DD)
              当为 None 时：公众号和 GitHub 用今天，论文用昨天
              当指定日期时：公众号和 GitHub 用该日期，论文用该日期的前一天
        dry_run: 只运行到格式化，不实际发布
    """
    # 确定日期
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    if date is None:
        # 使用混合日期策略
        wechat_date = today
        github_date = today
        papers_date = yesterday
        output_date = today  # 输出目录用今天
    else:
        # 用户指定日期：公众号和 GitHub 用指定日期，论文用前一天
        # （因为 HuggingFace 论文榜单只显示"昨天"的论文）
        specified_date = datetime.strptime(date, '%Y-%m-%d')
        papers_date = (specified_date - timedelta(days=1)).strftime('%Y-%m-%d')
        wechat_date = github_date = output_date = date

    print("=" * 60)
    print(f"🚀 DailyNews Pipeline - {output_date}")
    print(f"   公众号: {wechat_date} | GitHub: {github_date} | 论文: {papers_date}")
    print("=" * 60)

    # 初始化组件
    client = GeminiClient()
    formatter = MarkdownFormatter()
    llm_deduplicator = LLMDeduplicator(client)
    publisher = WechatPublisher()

    # 来源优先级映射
    priority_map = {"新智元": 3, "机器之心": 2, "量子位": 1}

    # 输出目录
    output_dir = PROJECT_ROOT / "output" / output_date
    summaries_dir = PROJECT_ROOT / "data" / "summaries" / output_date
    papers_summaries_dir = PROJECT_ROOT / "data" / "summaries" / papers_date

    # ========== Phase 1: 爬取 ==========
    print("\n" + "=" * 60)
    print("📡 Phase 1: Fetching")
    print("=" * 60)

    # 1.1 公众号文章 (默认今天)
    print(f"\n[1/3] 公众号文章 ({wechat_date})...")
    wechat_fetcher = WechatFetcher()
    try:
        articles = wechat_fetcher.fetch(wechat_date)
        print(f"  ✅ 爬取完成: {len(articles)} 篇")
    except Exception as e:
        print(f"  ❌ 爬取失败: {e}")
        articles = []

    # 1.2 GitHub Trending (默认今天)
    print(f"\n[2/3] GitHub Trending ({github_date})...")
    github_fetcher = GithubTrendingFetcher()
    try:
        repos = github_fetcher.fetch(github_date)
        # Save raw GitHub data
        if repos:
            github_fetcher.save_raw_data(repos, github_date)
            # Download README files
            github_fetcher.download_readmes(repos, date=github_date)
        print(f"  ✅ 爬取完成: {len(repos)} 个项目")
    except Exception as e:
        print(f"  ❌ 爬取失败: {e}")
        repos = []

    # 1.3 论文榜单 (默认昨天)
    print(f"\n[3/3] HuggingFace 论文 ({papers_date})...")
    papers_fetcher = PapersFetcher()
    try:
        papers = papers_fetcher.fetch(papers_date, max_papers=20)
        # Save raw papers data
        if papers:
            papers_fetcher.save_raw_data(papers, papers_date)
        print(f"  ✅ 获取完成: {len(papers)} 篇")
    except Exception as e:
        print(f"  ❌ 获取失败: {e}")
        papers = []

    # ========== Phase 2: 总结 ==========
    print("\n" + "=" * 60)
    print("🤖 Phase 2: Summarizing")
    print("=" * 60)

    summaries_dir.mkdir(parents=True, exist_ok=True)
    papers_summaries_dir.mkdir(parents=True, exist_ok=True)

    # 2.1 公众号文章总结
    article_summaries = []
    if not articles:
        # 如果内存中没有数据，尝试从 JSON 加载
        print("\n[1/3] 从 JSON 加载公众号文章...")
        articles = wechat_fetcher.load_from_json(wechat_date)

    if articles:
        print("\n[1/3] 公众号文章总结...")
        article_summarizer = ArticleSummarizer(client)
        articles_json_path = summaries_dir / "articles.json"
        article_summaries = article_summarizer.summarize_batch(articles, delay=1.0, output_path=str(articles_json_path))

        # 打分和 is_ad 现已集成到 ArticleSummarizer 中

    # 2.2 GitHub 项目总结
    github_summaries = []
    if repos:
        print("\n[2/3] GitHub 项目总结...")
        github_summarizer = GithubSummarizer(client, date=github_date)
        github_summaries = github_summarizer.summarize_batch(
            repos,
            delay=0.5,
            output_path=str(summaries_dir / "trending.json")
        )

    # 2.3 论文总结 (优先从内存，其次从 JSON 加载)
    print("\n[3/3] 论文榜单加载...")
    if not papers:
        papers = papers_fetcher.load_from_json(papers_date)

    paper_summaries = []
    if papers:
        # 使用 LLM 生成中文摘要
        paper_summarizer = PaperSummarizer(client)
        paper_summaries = paper_summarizer.summarize_batch_from_summary(
            papers,
            delay=1.0,
            output_path=str(papers_summaries_dir / "papers.json")
        )

        print(f"  ✅ 论文数据已保存 ({len(paper_summaries)} 篇)")

    # ========== Phase 3: LLM 去重 ==========
    print("\n" + "=" * 60)
    print("🔍 Phase 3: LLM Deduplication")
    print("=" * 60)

    # 3.1 公众号文章 LLM 去重
    print("\n[1/2] 公众号文章 LLM 去重...")
    before_count = len(article_summaries)
    cleaned_articles = llm_deduplicator.deduplicate(article_summaries, output_path=str(articles_json_path))
    after_count = len(cleaned_articles)
    print(f"  ✅ 去重完成: {before_count} → {after_count}")

    # 3.2 GitHub 项目通常不需要去重
    cleaned_repos = github_summaries

    # ========== Phase 4: 格式化（JSON → Markdown）==========
    print("\n" + "=" * 60)
    print("📝 Phase 4: Formatting")
    print("=" * 60)

    output_dir.mkdir(parents=True, exist_ok=True)
    papers_output_dir = PROJECT_ROOT / "output" / papers_date
    papers_output_dir.mkdir(parents=True, exist_ok=True)

    # 4.1 公众号日报
    if cleaned_articles:
        print("\n[1/3] 公众号日报...")
        daily_report = formatter.format_articles(cleaned_articles, output_date)
        formatter.save(daily_report, output_dir / "daily_report.md")

    # 4.2 GitHub Trending 报告
    if cleaned_repos:
        print("\n[2/3] GitHub Trending 报告...")
        trending_report = formatter.format_github(cleaned_repos, output_date)
        formatter.save(trending_report, output_dir / "github_trending.md")

    # 4.3 论文汇总
    if paper_summaries:
        print("\n[3/3] 论文汇总...")
        papers_report = formatter.format_papers_summary(paper_summaries, papers_date)
        formatter.save(papers_report, papers_output_dir / "papers_summary.md")

    # ========== Phase 5: 发布 ==========
    if dry_run:
        print("\n" + "=" * 60)
        print("🔍 DRY RUN - 跳过发布阶段")
        print("=" * 60)
        print(f"\n📁 输出目录: {output_dir}")
        print(f"📁 论文输出目录: {papers_output_dir}")
        print(f"📁 总结目录: {summaries_dir}")
        return

    print("\n" + "=" * 60)
    print("📤 Phase 5: Publishing")
    print("=" * 60)

    publish_errors = []

    # 5.1 发布公众号日报
    if cleaned_articles and (output_dir / "daily_report.md").exists():
        print("\n[1/3] 发布公众号日报...")
        try:
            result = publisher.publish_daily_report(
                str(output_dir / "daily_report.md"),
                target_date=output_date
            )
            print(f"  ✅ 草稿已创建: {result['draft_id']}")
        except Exception as e:
            print(f"  ❌ 发布失败: {e}")
            publish_errors.append(("daily_report", str(e)))

    # 5.2 发布 GitHub Trending
    if cleaned_repos and (output_dir / "github_trending.md").exists():
        print("\n[2/3] 发布 GitHub Trending...")
        try:
            result = publisher.publish_github_trending(
                str(output_dir / "github_trending.md"),
                target_date=github_date
            )
            print(f"  ✅ 草稿已创建: {result['draft_id']}")
        except Exception as e:
            print(f"  ❌ 发布失败: {e}")
            publish_errors.append(("github_trending", str(e)))

    # 5.3 发布论文汇总
    if paper_summaries and (papers_output_dir / "papers_summary.md").exists():
        print("\n[3/3] 发布论文汇总...")
        try:
            result = publisher.publish_papers_summary(
                str(papers_output_dir / "papers_summary.md"),
                target_date=papers_date
            )
            print(f"  ✅ 草稿已创建: {result['draft_id']}")
        except Exception as e:
            print(f"  ❌ 发布失败: {e}")
            publish_errors.append(("papers_summary", str(e)))

    # ========== 完成 ==========
    print("\n" + "=" * 60)
    print("✅ Pipeline Completed!")
    print("=" * 60)
    print(f"📁 输出目录: {output_dir}")
    print(f"📁 总结目录: {summaries_dir}")

    if publish_errors:
        print("\n⚠️ 发布错误:")
        for name, error in publish_errors:
            print(f"  - {name}: {error}")


def run_paper_analysis_pipeline(
    target_date: str = None,
    min_papers: int = 3,
    max_papers: int = 20,
    enable_topic_bonus: bool = False,
    dry_run: bool = False
):
    """
    论文深度分析流程 - 获取、排序、下载、分析

    Args:
        target_date: 目标日期 (YYYY-MM-DD)，默认昨天
        min_papers: 最少下载数
        max_papers: 最多下载数
        enable_topic_bonus: 是否启用兴趣加成
        dry_run: 只显示不实际执行
    """
    # 默认昨天
    if target_date is None:
        target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    print("=" * 80)
    print(f"Paper Analysis Pipeline - {target_date}")
    print("=" * 80)

    # 初始化组件
    client = GeminiClient()

    # 1. 获取并排序论文
    print(f"\n[1/5] 获取论文列表...")
    import requests
    url = f"https://huggingface.co/api/daily_papers?date={target_date}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if resp.status_code != 200:
        print(f"错误: API 请求失败 ({resp.status_code})")
        return

    papers = resp.json()
    if not papers:
        print(f"无数据: {target_date}")
        return

    print(f"  获取到 {len(papers)} 篇论文")

    # 2. 排序
    print(f"\n[2/5] 论文排序...")
    ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
    ranked = ranker.rank_papers(papers)

    # 找到最后一篇 Frontier Lab 论文的位置
    last_frontier_idx = 0
    for i, p in enumerate(ranked):
        reasons = p.get("rank_reasons", "")
        if "Super Lab" in reasons or "Frontier Lab" in reasons:
            last_frontier_idx = i

    # 统计 Frontier Lab 数量
    frontier_count = sum(1 for p in ranked[:last_frontier_idx+1]
                          if "Super Lab" in p.get("rank_reasons", "") or "Frontier Lab" in p.get("rank_reasons", ""))

    # 确定下载数量: 从第1篇到最后一篇 Frontier Lab
    download_count = max(min_papers, last_frontier_idx + 1)
    download_count = min(download_count, max_papers)

    papers_to_download = ranked[:download_count]
    print(f"  将下载: 第1篇 → 第{last_frontier_idx+1}篇 (共 {download_count} 篇)")
    print(f"  其中 Frontier Labs: {frontier_count} 篇")

    # 显示将要下载的论文列表
    print(f"\n  将分析的论文:")
    for i, p in enumerate(papers_to_download, 1):
        title = p.get("title", "")[:55]
        score = p.get("rank_score", 0)
        reasons = p.get("rank_reasons", "")
        marker = "🔥" if ("Super Lab" in reasons or "Frontier Lab" in reasons) else "  "
        print(f"    {i:2d}. [{marker}] {score:6.2f} | {title}... | {reasons}")

    if dry_run:
        print("\n[DRY RUN] 跳过实际下载和分析")
        return

    # 3. 准备目录
    download_dir = PROJECT_ROOT / "data" / target_date / "papers" / "pdf_downloads"
    download_dir.mkdir(parents=True, exist_ok=True)

    output_dir = PROJECT_ROOT / "output" / target_date
    output_dir.mkdir(parents=True, exist_ok=True)

    # 4. 下载 PDF
    print(f"\n[3/5] 下载 PDF...")
    downloaded_files = []

    import re
    import time

    for i, p in enumerate(papers_to_download, 1):
        paper = p.get("paper", {})
        arxiv_id = paper.get("id", "")
        title = p.get("title", "")
        score = p.get("rank_score", 0)
        reasons = p.get("rank_reasons", "")

        print(f"\n  [{i}/{download_count}] Score: {score} | {title[:60]}...")
        print(f"     Tags: {reasons}")

        # 下载 PDF
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
        filename = f"{arxiv_id}_{safe_title[:80]}.pdf"
        file_path = download_dir / filename

        if file_path.exists():
            print(f"    [已存在] {filename}")
        else:
            try:
                print(f"    [下载中] {filename}...")
                r = requests.get(
                    pdf_url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    stream=True,
                    timeout=60
                )
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    file_size = file_path.stat().st_size
                    print(f"    [完成] {file_size:,} bytes")
                    time.sleep(3)  # ArXiv 限制
                else:
                    print(f"    [失败] HTTP {r.status_code}")
                    continue
            except Exception as e:
                print(f"    [错误] {e}")
                continue

        downloaded_files.append({
            "pdf_path": file_path,
            "arxiv_id": arxiv_id,
            "title": title,
            "org": p.get("organization", {}).get("fullname", ""),
            "stars": paper.get("githubStars", 0),
            "upvotes": paper.get("upvotes", 0),
            "score": score,
            "reasons": reasons
        })

    if not downloaded_files:
        print("  没有成功下载任何论文")
        return

    # 5. 加载分析提示词
    prompt_path = PROJECT_ROOT / "prompt.md"
    if not prompt_path.exists():
        print("  ⚠️  未找到 prompt.md，使用默认提示词")
        prompt = "请用中文详细分析这篇论文，包括：核心贡献、方法论、创新点、实验结果、局限性等。"
    else:
        prompt = prompt_path.read_text(encoding='utf-8')

    # 6. 分析论文
    print(f"\n[4/5] 分析论文...")

    analysis_files = []

    for i, paper_info in enumerate(downloaded_files, 1):
        print(f"\n  论文 {i}/{len(downloaded_files)}")

        try:
            result = client.upload_and_analyze(str(paper_info["pdf_path"]), prompt)

            # 保存分析结果
            arxiv_id = paper_info.get("arxiv_id", "unknown")
            safe_title = re.sub(r'[\\/*?:"<>|]', "", paper_info.get('title', 'unknown')).strip()[:50]
            filename = f"{arxiv_id}_{safe_title}_analysis.md"
            output_path = output_dir / filename

            # 构建完整输出
            content = f"# {paper_info.get('title', 'Unknown')}\n\n"
            content += f"**arXiv ID**: {arxiv_id}\n"
            content += f"**组织**: {paper_info.get('org', 'Unknown')}\n"
            content += f"**GitHub Stars**: {paper_info.get('stars', 0)}\n"
            content += f"**Upvotes**: {paper_info.get('upvotes', 0)}\n"
            content += f"**得分**: {paper_info.get('score', 0)}\n"
            content += f"**标签**: {paper_info.get('reasons', 'N/A')}\n\n"
            content += "---\n\n"
            content += result

            output_path.write_text(content, encoding='utf-8')
            print(f"  [保存] {filename}")
            analysis_files.append(output_path)

        except Exception as e:
            print(f"  [错误] 分析失败: {e}")

    # 7. 汇总报告
    print(f"\n[5/5] 生成汇总报告...")
    summary_path = output_dir / "_summary.md"

    summary_content = f"# 每日论文分析报告 - {target_date}\n\n"
    summary_content += f"## 分析概览\n\n"
    summary_content += f"- **分析日期**: {target_date}\n"
    summary_content += f"- **论文数量**: {len(downloaded_files)}\n"
    summary_content += f"- **Frontier Labs**: {frontier_count}\n\n"
    summary_content += f"## 论文列表\n\n"

    for i, paper_info in enumerate(downloaded_files, 1):
        summary_content += f"{i}. **{paper_info['title'][:70]}...**\n"
        summary_content += f"   - 组织: {paper_info['org']}\n"
        summary_content += f"   - 得分: {paper_info['score']}\n"
        summary_content += f"   - 标签: {paper_info['reasons']}\n"
        arxiv_id = paper_info['arxiv_id']
        summary_content += f"   - 分析: [{arxiv_id}_analysis.md]({arxiv_id}_analysis.md)\n\n"

    summary_path.write_text(summary_content, encoding='utf-8')

    print("\n" + "=" * 80)
    print("Pipeline 完成!")
    print(f"  下载目录: {download_dir}")
    print(f"  输出目录: {output_dir}")
    print(f"  分析文件: {len(analysis_files)} 篇")
    print("=" * 80)

    return {
        'download_dir': str(download_dir),
        'output_dir': str(output_dir),
        'count': len(analysis_files)
    }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="DailyNews 全自动流程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      # 运行默认策略（公众号/GitHub今天，论文昨天）
  python main.py 2026-02-01           # 所有模块统一使用指定日期
  python main.py --dry-run            # 只运行到格式化，不发布
  python main.py --fetch-only         # 只爬取数据（使用默认日期策略）
  python main.py --summarize-only     # 只总结数据（从 JSON 加载已爬取的数据）
  python main.py --analyze-papers     # 运行论文深度分析流程
  python main.py --analyze-papers --date 2026-01-30 --min-papers 5 --max-papers 15
        """
    )

    parser.add_argument(
        'date',
        nargs='?',
        help='目标日期 (YYYY-MM-DD)，默认使用混合策略（公众号/GitHub今天，论文昨天）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='只运行到格式化阶段，不实际发布'
    )
    parser.add_argument(
        '--fetch-only',
        action='store_true',
        help='只爬取数据，不进行总结和发布'
    )
    parser.add_argument(
        '--summarize-only',
        action='store_true',
        help='只总结数据（从 JSON 加载已爬取的数据），不爬取和发布'
    )

    # 论文深度分析选项
    parser.add_argument(
        '--analyze-papers',
        action='store_true',
        help='运行论文深度分析流程（下载PDF + Gemini分析）'
    )
    parser.add_argument(
        '--min-papers',
        type=int,
        default=3,
        help='最少下载论文数 (默认3，仅在--analyze-papers时有效)'
    )
    parser.add_argument(
        '--max-papers',
        type=int,
        default=20,
        help='最多下载论文数 (默认20，仅在--analyze-papers时有效)'
    )
    parser.add_argument(
        '--topic-bonus',
        action='store_true',
        help='启用论文兴趣加成 (仅在--analyze-papers时有效)'
    )
    parser.add_argument(
        '--publish-papers',
        action='store_true',
        help='分析完成后将每篇论文发布为独立草稿 (需与--analyze-papers一起使用)'
    )

    args = parser.parse_args()

    try:
        # 论文深度分析模式
        if args.analyze_papers:
            result = run_paper_analysis_pipeline(
                target_date=args.date,
                min_papers=args.min_papers,
                max_papers=args.max_papers,
                enable_topic_bonus=args.topic_bonus,
                dry_run=args.dry_run
            )

            # 如果需要发布论文
            if not args.dry_run and args.publish_papers and result:
                print("\n" + "=" * 60)
                print("📤 发布论文分析...")
                print("=" * 60)
                publisher = WechatPublisher()
                date_str = args.date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                results = publisher.publish_all_papers(date_str)
                success_count = sum(1 for r in results if r.get('status') == 'success')
                print(f"\n✅ 完成: {success_count}/{len(results)} 篇论文发布成功")
            return

        if args.summarize_only:
            # 只运行总结阶段（从 JSON 加载数据）
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            wechat_date = github_date = today
            papers_date = yesterday

            # 如果用户指定了日期
            if args.date:
                specified_date = datetime.strptime(args.date, '%Y-%m-%d')
                papers_date = (specified_date - timedelta(days=1)).strftime('%Y-%m-%d')
                wechat_date = github_date = args.date

            print(f"🤖 只总结数据")
            print(f"   公众号: {wechat_date} | GitHub: {github_date} | 论文: {papers_date}")

            # 初始化
            client = GeminiClient()
            formatter = MarkdownFormatter()
            llm_deduplicator = LLMDeduplicator(client)

            priority_map = {"新智元": 3, "机器之心": 2, "量子位": 1}
            output_dir = PROJECT_ROOT / "output" / wechat_date
            summaries_dir = PROJECT_ROOT / "data" / "summaries" / wechat_date
            papers_summaries_dir = PROJECT_ROOT / "data" / "summaries" / papers_date
            summaries_dir.mkdir(parents=True, exist_ok=True)
            papers_summaries_dir.mkdir(parents=True, exist_ok=True)

            # 1. 公众号文章
            wechat_fetcher = WechatFetcher()
            articles = wechat_fetcher.load_from_json(wechat_date)

            article_summaries = []
            if articles:
                article_summarizer = ArticleSummarizer(client)
                articles_json_path = summaries_dir / "articles.json"
                article_summaries = article_summarizer.summarize_batch(articles, delay=1.0, output_path=str(articles_json_path))

                # 打分和 is_ad 现已集成到 ArticleSummarizer 中

            # 2. GitHub Trending
            github_fetcher = GithubTrendingFetcher()
            repos = github_fetcher._load_from_json(github_date)

            github_summaries = []
            if repos:
                github_summarizer = GithubSummarizer(client, date=github_date)
                github_summaries = github_summarizer.summarize_batch(
                    repos,
                    delay=0.5,
                    output_path=str(summaries_dir / "trending.json")
                )

            # 3. 论文 - 加载所有论文用于每日报告
            papers_fetcher = PapersFetcher()
            papers = papers_fetcher.load_from_json(papers_date)

            paper_summaries = []
            if papers:
                # 使用 LLM 生成中文摘要
                paper_summarizer = PaperSummarizer(client)
                paper_summaries = paper_summarizer.summarize_batch_from_summary(
                    papers,
                    delay=1.0,
                    output_path=str(papers_summaries_dir / "papers.json")
                )

            # 4. LLM 去重
            cleaned_articles = llm_deduplicator.deduplicate(article_summaries, output_path=str(articles_json_path))

            # 5. 格式化输出
            output_dir.mkdir(parents=True, exist_ok=True)
            papers_output_dir = PROJECT_ROOT / "output" / papers_date
            papers_output_dir.mkdir(parents=True, exist_ok=True)

            if cleaned_articles:
                daily_report = formatter.format_articles(cleaned_articles, wechat_date)
                formatter.save(daily_report, output_dir / "daily_report.md")

            if github_summaries:
                trending_report = formatter.format_github(github_summaries, wechat_date)
                formatter.save(trending_report, output_dir / "github_trending.md")

            if paper_summaries:
                papers_report = formatter.format_papers_summary(paper_summaries, papers_date)
                formatter.save(papers_report, papers_output_dir / "papers_summary.md")

            print("\n✅ 总结完成")
            print(f"📁 输出目录: {output_dir}")
            return

        if args.fetch_only:
            # 只运行爬取阶段（使用混合日期策略）
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            wechat_date = github_date = today
            papers_date = yesterday

            # 如果用户指定了日期，公众号和 GitHub 用该日期，论文用前一天
            if args.date:
                specified_date = datetime.strptime(args.date, '%Y-%m-%d')
                papers_date = (specified_date - timedelta(days=1)).strftime('%Y-%m-%d')
                wechat_date = github_date = args.date

            print(f"📡 只爬取数据")
            print(f"   公众号: {wechat_date} | GitHub: {github_date} | 论文: {papers_date}")

            wechat_fetcher = WechatFetcher()
            articles = wechat_fetcher.fetch(wechat_date)
            if articles:
                wechat_fetcher.save_raw_data(articles, wechat_date)

            github_fetcher = GithubTrendingFetcher()
            repos = github_fetcher.fetch(github_date)
            if repos:
                github_fetcher.save_raw_data(repos, github_date)
                # 下载 README
                github_fetcher.download_readmes(repos, date=github_date)

            papers_fetcher = PapersFetcher()
            papers = papers_fetcher.fetch(papers_date)
            if papers:
                # 先下载 PDF（让 download_pdfs 使用自己的裁剪逻辑）
                papers_fetcher.download_pdfs(papers, date=papers_date)
                # 获取实际下载的论文数量，用于保存 JSON
                last_frontier_idx = 0
                for i, p in enumerate(papers):
                    reasons = p.get("rank_reasons", "")
                    if "Super Lab" in reasons or "Frontier Lab" in reasons:
                        last_frontier_idx = i
                # 使用与 download_pdfs 相同的裁剪逻辑
                download_count = max(3, last_frontier_idx + 1)
                download_count = min(download_count, 12)
                papers_to_save = papers[:download_count]
                papers_fetcher.save_raw_data(papers_to_save, papers_date)

            print("\n✅ 爬取完成")

        else:
            run_pipeline(date=args.date, dry_run=args.dry_run)

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
