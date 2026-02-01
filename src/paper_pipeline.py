#!/usr/bin/env python3
"""
Paper Analysis Pipeline

完整流程:
1. 获取 HuggingFace Daily Papers
2. 使用 PaperRanker 排序
3. 下载论文 (从第1篇到最后一篇 Frontier Lab，最少1-3篇)
4. 逐个分析论文 (使用 Gemini)
5. 输出到 output/{date}/ 文件夹
"""
import os
import sys
import time
import requests
from datetime import date, timedelta
from pathlib import Path

# 清除代理环境变量 (避免影响 requests)
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(proxy_var, None)

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.paper_ranker import PaperRanker
from src.gemini_client import GeminiClient


def load_prompt(prompt_path: str = None) -> str:
    """加载分析提示词"""
    if prompt_path is None:
        prompt_path = Path(__file__).parent.parent / "prompt.md"
    return Path(prompt_path).read_text(encoding='utf-8')


def download_pdf(arxiv_id: str, title: str, save_dir: Path) -> Path | None:
    """下载单篇论文 PDF"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # 清理文件名
    import re
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
    filename = f"{arxiv_id}_{safe_title[:80]}.pdf"
    file_path = save_dir / filename

    if file_path.exists():
        print(f"    [已存在] {filename}")
        return file_path

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
            return None
    except Exception as e:
        print(f"    [错误] {e}")
        return None

    return file_path


def analyze_paper(pdf_path: Path, prompt: str, client: GeminiClient) -> str:
    """分析单篇论文"""
    print(f"\n  分析中: {pdf_path.name}")
    result = client.upload_and_analyze(str(pdf_path), prompt)
    return result


def save_analysis(paper_info: dict, analysis: str, output_dir: Path) -> Path:
    """保存分析结果"""
    import re
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
    content += analysis

    output_path.write_text(content, encoding='utf-8')
    print(f"  [保存] {filename}")
    return output_path


def run_pipeline(
    target_date: str,
    min_papers: int = 3,
    max_papers: int = 20,
    enable_topic_bonus: bool = False,
    dry_run: bool = False
):
    """
    运行完整 pipeline

    Args:
        target_date: 目标日期 (YYYY-MM-DD)
        min_papers: 最少下载数
        max_papers: 最多下载数 (防止下载太多)
        enable_topic_bonus: 是否启用兴趣加成
        dry_run: 只显示不实际执行 (测试用)
    """
    print("=" * 80)
    print(f"Paper Analysis Pipeline - {target_date}")
    print("=" * 80)

    # 1. 获取并排序论文
    print(f"\n[1/5] 获取论文列表...")
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
    # 至少 min_papers 篇，最多 max_papers 篇
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
    project_root = Path(__file__).parent.parent
    download_dir = project_root / "HF_Paper_Downloads" / target_date
    download_dir.mkdir(parents=True, exist_ok=True)

    output_dir = project_root / "output" / target_date
    output_dir.mkdir(parents=True, exist_ok=True)

    # 4. 下载 PDF
    print(f"\n[3/5] 下载 PDF...")
    downloaded_files = []

    for i, p in enumerate(papers_to_download, 1):
        paper = p.get("paper", {})
        arxiv_id = paper.get("id", "")
        title = p.get("title", "")
        score = p.get("rank_score", 0)
        reasons = p.get("rank_reasons", "")

        print(f"\n  [{i}/{download_count}] Score: {score} | {title[:60]}...")
        print(f"     Tags: {reasons}")

        pdf_path = download_pdf(arxiv_id, title, download_dir)
        if pdf_path:
            downloaded_files.append({
                "pdf_path": pdf_path,
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

    # 5. 分析论文
    print(f"\n[4/5] 分析论文...")
    client = GeminiClient()
    prompt = load_prompt()

    analysis_files = []

    for i, paper_info in enumerate(downloaded_files, 1):
        print(f"\n  论文 {i}/{len(downloaded_files)}")

        try:
            analysis = analyze_paper(paper_info["pdf_path"], prompt, client)
            output_path = save_analysis(paper_info, analysis, output_dir)
            analysis_files.append(output_path)
        except Exception as e:
            print(f"  [错误] 分析失败: {e}")

    # 6. 汇总报告
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
        summary_content += f"   - 分析: [{paper_info['arxiv_id']}_analysis.md]({paper_info['arxiv_id']}_analysis.md)\n\n"

    summary_path.write_text(summary_content, encoding='utf-8')

    print("\n" + "=" * 80)
    print("Pipeline 完成!")
    print(f"  下载目录: {download_dir}")
    print(f"  输出目录: {output_dir}")
    print(f"  分析文件: {len(analysis_files)} 篇")
    print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Paper Analysis Pipeline")
    parser.add_argument("--date", default=None, help="目标日期 (YYYY-MM-DD)，默认昨天")
    parser.add_argument("--min-papers", type=int, default=3, help="最少下载数 (默认3)")
    parser.add_argument("--max-papers", type=int, default=20, help="最多下载数 (默认20)")
    parser.add_argument("--topic-bonus", action="store_true", help="启用兴趣加成")
    parser.add_argument("--dry-run", action="store_true", help="只显示不实际执行")

    args = parser.parse_args()

    # 默认昨天
    if args.date:
        target_date = args.date
    else:
        target_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    run_pipeline(
        target_date=target_date,
        min_papers=args.min_papers,
        max_papers=args.max_papers,
        enable_topic_bonus=args.topic_bonus,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
