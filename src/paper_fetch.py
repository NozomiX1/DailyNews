"""
Paper Fetcher - 从 HuggingFace 获取每日论文榜单

使用 PaperRanker 对论文进行评分排序，保存为 Markdown。
"""
import os
import sys
import requests
from datetime import date, timedelta
from pathlib import Path

# 清除代理环境变量 (避免影响 requests)
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy_var, None)

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.paper_ranker import PaperRanker

# ArXiv 对爬虫限制较严，必须带 User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    import re
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def fetch_and_save_papers(target_date: str, max_papers: int = 20, enable_topic_bonus: bool = False) -> Path:
    """
    获取指定日期的论文并保存为 Markdown

    Args:
        target_date: 目标日期 (YYYY-MM-DD)
        max_papers: 最多保存论文数
        enable_topic_bonus: 是否启用兴趣加成

    Returns:
        保存的文件路径
    """
    # 1. 获取论文列表
    print(f"[1/3] 获取论文列表: {target_date}")
    url = f"https://huggingface.co/api/daily_papers?date={target_date}"
    resp = requests.get(url, headers=HEADERS, timeout=30)

    if resp.status_code != 200:
        raise Exception(f"API 请求失败 ({resp.status_code}): {url}")

    papers = resp.json()
    if not papers:
        raise Exception(f"当日无数据: {target_date}")

    print(f"  获取到 {len(papers)} 篇论文")

    # 2. 排序
    print(f"\n[2/3] 论文排序...")
    ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
    ranked = ranker.rank_papers(papers)

    # 保存到 data/papers/ 目录
    papers_dir = Path(__file__).parent.parent / "data" / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)

    output_path = papers_dir / f"{target_date}.md"

    # 3. 生成 Markdown
    print(f"\n[3/3] 保存榜单...")
    content = f"# 每日论文榜单 - {target_date}\n\n"
    content += f"**日期**: {target_date}\n"
    content += f"**论文数**: {len(ranked)}\n\n"
    content += "---\n\n"

    for i, paper in enumerate(ranked[:max_papers], 1):
        title = paper.get("title", "Unknown")
        org = paper.get("organization", {}).get("fullname", "Unknown")
        score = paper.get("rank_score", 0)
        reasons = paper.get("rank_reasons", "")
        is_golden = paper.get("is_golden", False)

        paper_detail = paper.get("paper", {})
        arxiv_id = paper_detail.get("id", "")
        upvotes = paper_detail.get("upvotes", 0)
        stars = paper_detail.get("githubStars", 0)
        comments = paper.get("numComments", 0)
        summary = paper_detail.get("summary", "") or paper.get("summary", "")

        # 标题行
        golden_mark = "🏆" if is_golden else ""
        content += f"### {golden_mark} {i}. {title}\n\n"

        # 元信息
        content += f"**arXiv ID**: {arxiv_id}\n"
        content += f"**组织**: {org}\n"
        content += f"**得分**: {score}\n"
        content += f"**标签**: {reasons}\n"
        content += f"**Upvotes**: {upvotes} | **Stars**: {stars} | **Comments**: {comments}\n\n"

        # 摘要
        if summary:
            content += f"**摘要**: {summary[:300]}...\n\n"

        content += "---\n\n"

    output_path.write_text(content, encoding='utf-8')
    print(f"  已保存: {output_path}")

    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="获取 HuggingFace 每日论文榜单")
    parser.add_argument("--date", default=None, help="日期 (YYYY-MM-DD)，默认昨天")
    parser.add_argument("--max-papers", type=int, default=20, help="最多保存论文数")
    parser.add_argument("--topic-bonus", action="store_true", help="启用兴趣加成")

    args = parser.parse_args()

    # 默认昨天
    target_date = args.date or (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    print("=" * 60)
    print(f"📊 HuggingFace 每日论文榜单")
    print(f"📅 日期: {target_date}")
    print("=" * 60)

    try:
        output_path = fetch_and_save_papers(
            target_date,
            max_papers=args.max_papers,
            enable_topic_bonus=args.topic_bonus
        )
        print(f"\n✅ 完成!")
        print(f"📄 文件: {output_path}")

    except Exception as e:
        print(f"\n❌ 失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
