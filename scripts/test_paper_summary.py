#!/usr/bin/env python3
"""
Test script for paper summary generation.

Tests the system prompt fix by summarizing all papers from existing data
and generating the papers_summary.md file.
"""
import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.summarizers import PaperSummarizer, GeminiClient
from src.processors import MarkdownFormatter


def main():
    # Load existing papers data
    papers_path = PROJECT_ROOT / "data" / "2026-01-30" / "papers" / "2026-01-30.json"

    with open(papers_path, 'r', encoding='utf-8') as f:
        all_papers = json.load(f)

    print(f"🧪 Testing with {len(all_papers)} papers")
    print("=" * 60)

    # Initialize client and summarizer
    client = GeminiClient()
    summarizer = PaperSummarizer(client)
    formatter = MarkdownFormatter()

    # Run summarization
    results = summarizer.summarize_batch_from_summary(
        all_papers,
        delay=1.0,
        output_path=str(PROJECT_ROOT / "data" / "summaries" / "test_papers.json")
    )

    # Generate Markdown report
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    papers_report = formatter.format_papers_summary(results, "2026-01-30")
    formatter.save(papers_report, output_dir / "test_papers_summary.md")

    # Verify results
    print("\n" + "=" * 60)
    print("📊 Results Verification:")
    print("=" * 60)

    success_count = 0
    for i, result in enumerate(results, 1):
        has_summary = bool(result.get('summary_zh'))
        if has_summary:
            success_count += 1

        print(f"\n[{i}] {result.get('title', 'Unknown')[:50]}...")
        print(f"  - title_zh: {result.get('title_zh', 'N/A')[:30]}...")
        print(f"  - summary_zh: {result.get('summary_zh', 'EMPTY')[:50]}...")
        print(f"  - relevance: {result.get('relevance', 'N/A')}")
        print(f"  - highlights: {len(result.get('highlights', []))} items")
        print(f"  {'  ✅ PASS' if has_summary else '  ❌ FAIL'}")

    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{len(results)} papers have summary_zh")
    print(f"📁 JSON: data/summaries/test_papers.json")
    print(f"📁 Markdown: output/test_papers_summary.md")


if __name__ == "__main__":
    main()
