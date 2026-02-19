#!/usr/bin/env python3
"""
Test script for Zhipu GLM 4.7 Flash article summarization.

Usage:
    python scripts/test_zhipu_summarizer.py

This script reads yesterday's WeChat articles and summarizes them
using the ZhipuClient to test GLM 4.7 Flash's performance.
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.summarizers.zhipu_client import ZhipuClient
from src.summarizers.article_summarizer import ArticleSummarizer


def get_test_articles():
    """Get test articles from yesterday's daily report."""
    # Use yesterday's backup report
    report_path = PROJECT_ROOT / "output" / "2026-02-18-backup" / "daily_report.md"

    if not report_path.exists():
        print(f"❌ 找不到测试文件: {report_path}")
        return []

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse articles from the report
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
                title_line = line[4:].strip()
                break

        if not title_line:
            continue

        # Extract metadata
        source = ""
        url = ""
        for line in lines:
            if line.startswith("**来源**:"):
                source = line.replace("**来源**:", "").strip()
            elif line.startswith("**链接**:"):
                url = line.replace("**链接**:", "").strip()

        # Get summary content (skip metadata lines)
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
            "content": summary_content,
        })

    return articles


def main():
    """Main test function."""
    print("=" * 60)
    print("🧪 Zhipu GLM 4.7 Flash 文章摘要测试")
    print("=" * 60)

    # Initialize Zhipu client
    print("\n📦 初始化 ZhipuClient...")
    try:
        client = ZhipuClient(model="glm-4-flash")
        print("✅ ZhipuClient 初始化成功")
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        print("💡 请设置 ZHIPU_API_KEY 环境变量")
        return

    # Get test articles
    print("\n📄 加载测试文章...")
    articles = get_test_articles()

    if not articles:
        print("❌ 没有找到测试文章")
        return

    print(f"✅ 找到 {len(articles)} 篇文章")

    # Test with first article only for quick validation
    print("\n" + "=" * 60)
    print("📝 测试第一篇文章摘要...")
    print("=" * 60)

    test_article = articles[0]
    print(f"\n文章标题: {test_article['title']}")
    print(f"来源: {test_article['source']}")

    # Create summarizer with Zhipu client
    summarizer = ArticleSummarizer(client)

    print("\n🤖 正在生成摘要...")

    try:
        result = summarizer.summarize(
            content=test_article["content"],
            metadata={
                "title": test_article["title"],
                "account": test_article["source"],
                "url": test_article["url"],
            }
        )

        print("\n" + "=" * 60)
        print("✅ 摘要生成成功")
        print("=" * 60)

        print(f"\n标题: {result.get('title', 'N/A')}")
        print(f"标签: {result.get('tags', [])}")
        print(f"评分: {'🌟' * result.get('score', 0)}")
        print(f"广告: {'是' if result.get('is_ad') else '否'}")
        print(f"\n摘要:\n{result.get('summary', 'N/A')}")

        # Save result
        output_dir = PROJECT_ROOT / "test_output" / "2026-02-18-zhipu"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "summary_result.json"

        import json
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 结果已保存到: {output_file}")

    except Exception as e:
        print(f"\n❌ 摘要生成失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
