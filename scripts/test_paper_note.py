#!/usr/bin/env python3
"""
Test script for paper note generation (PDF analysis).

Analyzes a single paper PDF to generate detailed research notes.
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
    # Configuration
    DATE = "2026-01-30"
    ARXIV_ID = "2601.21571"  # Shaping capabilities with token-level data filtering

    # Paths
    papers_json_path = PROJECT_ROOT / "data" / DATE / "papers" / f"{DATE}.json"
    pdf_dir = PROJECT_ROOT / "data" / DATE / "papers" / "pdf_downloads"
    output_dir = PROJECT_ROOT / "output"

    # Load papers data
    with open(papers_json_path, 'r', encoding='utf-8') as f:
        all_papers = json.load(f)

    # Find the target paper
    target_paper = None
    for paper in all_papers:
        paper_id = paper.get('paper', {}).get('id', '')
        if paper_id == ARXIV_ID:
            target_paper = paper
            break

    if not target_paper:
        print(f" Paper {ARXIV_ID} not found!")
        return

    # Find PDF path
    pdf_path = None
    for pdf_file in pdf_dir.glob("*.pdf"):
        if ARXIV_ID in pdf_file.name:
            pdf_path = pdf_file
            break

    if not pdf_path:
        print(f" PDF not found for {ARXIV_ID}!")
        return

    print(f" Testing Paper Note Generation")
    print("=" * 60)
    print(f"Paper: {target_paper.get('title', 'Unknown')}")
    print(f"arXiv ID: {ARXIV_ID}")
    print(f"PDF: {pdf_path.name}")
    print("=" * 60)

    # Initialize summarizer with full prompt for PDF analysis
    client = GeminiClient()
    summarizer = PaperSummarizer(client, load_full_prompt=True)

    # Analyze PDF
    print("\n Starting PDF analysis...")
    result = summarizer.summarize(str(pdf_path), target_paper)

    # Output result
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"paper_note_{ARXIV_ID.replace('.', '_')}.md"

    formatter = MarkdownFormatter()

    # Build markdown content
    content = f"# {result.get('title', 'Unknown')}\n\n"
    content += f"**arXiv ID**: [{result.get('arxiv_id', '')}](https://arxiv.org/abs/{result.get('arxiv_id', '')})\n"
    content += f"**组织**: {result.get('org', 'Unknown')}\n"
    content += f"**得分**: {result.get('score', 0)}\n"
    content += f"**Upvotes**: {result.get('upvotes', 0)} | **Stars**: {result.get('stars', 0)}\n\n"
    content += "---\n\n"
    content += result.get('analysis', '')

    formatter.save(content, output_path)

    print("\n" + "=" * 60)
    print(f" Paper note saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
