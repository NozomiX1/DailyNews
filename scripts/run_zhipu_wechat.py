#!/usr/bin/env python3
"""
使用 Zhipu GLM 4.7 Flash 运行完整的公众号文章处理流程

流程:
1. 爬取/加载文章
2. LLM 总结
3. LLM 去重
4. 生成 Markdown 报告

Usage:
    python scripts/run_zhipu_wechat.py [--date 2026-02-18]
"""
import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.summarizers.zhipu_client import ZhipuClient
from src.summarizers.article_summarizer import ArticleSummarizer
from src.processors.llm_deduplicator import LLMDeduplicator
from src.processors.formatter import MarkdownFormatter

# 配置
ZHIPU_MODEL = "glm-4.7"  # 使用新的 GLM-5 模型
MAX_TOKENS = 65536
DELAY_BETWEEN_REQUESTS = 3.0  # GLM API 请求间隔


def load_articles_from_backup(date: str) -> list:
    """从备份的 daily_report.md 解析文章（作为后备方案）"""
    # 尝试多个可能的备份路径
    possible_paths = [
        PROJECT_ROOT / "output" / f"{date}-backup" / "daily_report.md",
        PROJECT_ROOT / "output" / date / "daily_report.md",
    ]

    backup_path = None
    for path in possible_paths:
        if path.exists():
            backup_path = path
            break

    if not backup_path:
        print(f"❌ 找不到备份文件，尝试过: {possible_paths}")
        return []

    print(f"  📂 使用备份: {backup_path}")

    with open(backup_path, "r", encoding="utf-8") as f:
        content = f.read()

    articles = []
    sections = content.split("---")

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        if not lines:
            continue

        # Find title line (starts with ###)
        title_line = None
        for line in lines:
            if line.startswith("### "):
                # Remove number prefix like "1. "
                title_line = line[4:].strip()
                if title_line[0].isdigit() and ". " in title_line[:4]:
                    title_line = title_line.split(". ", 1)[1]
                break

        if not title_line:
            continue

        # Extract metadata
        source = ""
        url = ""
        time_str = ""
        tags = []
        score = 3

        for line in lines:
            if line.startswith("**来源**:"):
                source_raw = line.replace("**来源**:", "").strip()
                # Split by | to get source and time
                if " | " in source_raw:
                    parts = source_raw.split(" | ")
                    source = parts[0].strip()
                    for part in parts[1:]:
                        if "**时间**:" in part or "时间:" in part:
                            time_str = part.replace("**时间**:", "").replace("时间:", "").strip()
                else:
                    source = source_raw
            elif line.startswith("**链接**:"):
                url = line.replace("**链接**:", "").strip()
            elif line.startswith("**标签**:"):
                tags_str = line.replace("**标签**:", "").strip()
                # Parse tags like [tag1] [tag2]
                import re
                tags = re.findall(r'\[([^\]]+)\]', tags_str)
            elif line.startswith("**价值**:"):
                # Count stars
                score = line.count("🌟")

        # Get summary content (from blockquote onwards)
        summary_start = False
        summary_lines = []
        for line in lines:
            if line.startswith("> "):
                summary_start = True
            if summary_start:
                summary_lines.append(line)

        summary_content = "\n".join(summary_lines)

        articles.append({
            "title": title_line,
            "source": source,
            "url": url,
            "time_str": time_str,
            "timestamp": 0,
            "tags": tags,
            "score": score,
            "content": summary_content,  # Use existing summary as content
        })

    return articles


def fetch_fresh_articles(date: str) -> list:
    """尝试爬取新鲜文章"""
    try:
        from src.fetchers.wechat import WechatFetcher
        import config

        fetcher = WechatFetcher(data_dir=PROJECT_ROOT / "data")
        articles = fetcher.fetch(date)
        return articles
    except Exception as e:
        print(f"⚠️ 爬取失败: {e}")
        print("   将使用备份数据...")
        return []


def summarize_articles(client: ZhipuClient, articles: list) -> list:
    """使用 Zhipu 总结文章"""
    print(f"\n[2/4] 使用 GLM 4.7 Flash 总结文章...")

    summarizer = ArticleSummarizer(client)
    summaries = []

    total = len(articles)
    for i, article in enumerate(articles, 1):
        title = article.get('title', article.get('original_title', ''))
        print(f"  [{i}/{total}] {title[:40]}...")

        content = article.get('content', '')
        if not content or len(content) < 100:
            print(f"      ⚠️ 内容过短，跳过")
            continue

        try:
            result = summarizer.summarize(content, article)
            summaries.append(result)
            score = result.get('score', 0)
            stars = '🌟' * score if score > 0 else 'N/A'
            print(f"      ✅ 标签: {result.get('tags')} | 评分: {stars}")
        except Exception as e:
            print(f"      ❌ 总结失败: {e}")
            # Add fallback
            summaries.append({
                'title': title[:50] + '...' if len(title) > 50 else title,
                'tags': ['未分类'],
                'summary': f"总结失败: {str(e)}",
                'score': 1,
                'is_ad': False,
                'source': article.get('source', ''),
                'url': article.get('url', ''),
                'original_title': title,
            })

        # Rate limiting
        if i < total:
            import time
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"  ✅ 总结完成，共 {len(summaries)} 篇")
    return summaries


def deduplicate_articles(client: ZhipuClient, summaries: list) -> list:
    """使用 LLM 去重"""
    print(f"\n[3/4] LLM 去重...")

    deduplicator = LLMDeduplicator(client)
    before_count = len(summaries)

    try:
        cleaned = deduplicator.deduplicate(summaries)
        after_count = len(cleaned)
        print(f"  ✅ 去重完成: {before_count} → {after_count}")
        return cleaned
    except Exception as e:
        print(f"  ⚠️ 去重失败: {e}，返回原始数据")
        return summaries


def generate_report(summaries: list, date: str) -> str:
    """生成 Markdown 报告"""
    print(f"\n[4/4] 生成 Markdown 报告...")

    formatter = MarkdownFormatter()
    content = formatter.format_articles(summaries, date)

    # Save to file
    output_dir = PROJECT_ROOT / "test_output" / f"{date}-zhipu"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "daily_report.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  💾 已保存: {output_path}")

    # Also save JSON
    json_path = output_dir / "articles.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    print(f"  💾 已保存: {json_path}")

    return content


def main():
    parser = argparse.ArgumentParser(description="使用 Zhipu GLM 运行公众号文章流程")
    parser.add_argument("--date", default="2026-02-18", help="目标日期 (YYYY-MM-DD)")
    parser.add_argument("--use-backup", action="store_true", help="直接使用备份数据，不爬取")
    args = parser.parse_args()

    date = args.date

    print("=" * 60)
    print(f"🧪 Zhipu GLM-5 公众号文章处理测试")
    print(f"📅 日期: {date}")
    print("=" * 60)

    # Initialize Zhipu client
    print("\n📦 初始化 ZhipuClient...")
    print(f"   模型: {ZHIPU_MODEL}")
    print(f"   Temperature: 1.0")
    print(f"   Max Tokens: {MAX_TOKENS}")

    try:
        client = ZhipuClient(
            model=ZHIPU_MODEL,
            max_tokens=MAX_TOKENS,
            enable_thinking=False,
        )
        print("✅ ZhipuClient 初始化成功")
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        print("💡 请设置 ZHIPU_API_KEY 环境变量")
        return

    # Step 1: 获取文章
    print(f"\n[1/4] 获取文章...")

    if args.use_backup:
        articles = load_articles_from_backup(date)
    else:
        # Try fresh fetch first, fallback to backup
        articles = fetch_fresh_articles(date)
        if not articles:
            articles = load_articles_from_backup(date)

    if not articles:
        print("❌ 没有找到文章")
        return

    print(f"✅ 找到 {len(articles)} 篇文章")

    # Step 2: Summarize
    summaries = summarize_articles(client, articles)

    # Step 3: Deduplicate
    cleaned = deduplicate_articles(client, summaries)

    # Step 4: Generate report
    content = generate_report(cleaned, date)

    print("\n" + "=" * 60)
    print("✅ 处理完成！")
    print("=" * 60)

    # Print preview
    print(f"\n📄 报告预览 (前500字符):")
    print("-" * 50)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-" * 50)


if __name__ == "__main__":
    main()
