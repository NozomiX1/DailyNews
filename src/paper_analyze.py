#!/usr/bin/env python3
"""
Paper Analysis Tool using Gemini API

Analyzes academic papers in PDF format using Google's Gemini AI.
Loads analysis prompt from prompt.md and saves results to markdown.

Usage:
    python -m src.paper_analyze path/to/paper.pdf
    python -m src.paper_analyze path/to/paper.pdf -o output.md
"""
import argparse
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gemini_client import GeminiClient


def load_prompt(prompt_path: str = None) -> str:
    """Load analysis prompt from file."""
    if prompt_path is None:
        prompt_path = Path(__file__).parent.parent / "prompt.md"

    prompt_file = Path(prompt_path)
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_file.read_text(encoding='utf-8')


def analyze_paper(
    pdf_path: str,
    output_path: str | None = None,
    prompt_path: str = None,
    model: str = "gemini-3-pro-high"
) -> str:
    """
    Analyze a paper PDF and save the analysis.

    Args:
        pdf_path: Path to the PDF file
        output_path: Output markdown file (default: {pdf_stem}_analysis.md)
        prompt_path: Path to the prompt template file
        model: Gemini model to use

    Returns:
        The analysis result text
    """
    # Initialize client
    client = GeminiClient(model=model)

    # Load prompt
    prompt = load_prompt(prompt_path)

    # Analyze
    print(f"Analyzing: {pdf_path}")
    result = client.upload_and_analyze(pdf_path, prompt)

    # Determine output path
    if output_path is None:
        pdf_stem = Path(pdf_path).stem
        output_path = f"{pdf_stem}_analysis.md"

    # Save result
    Path(output_path).write_text(result, encoding='utf-8')
    print(f"Analysis saved to: {output_path}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Analyze academic papers using Gemini AI"
    )
    parser.add_argument(
        "pdf",
        help="Path to the PDF file to analyze"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output markdown file (default: {pdf_stem}_analysis.md)"
    )
    parser.add_argument(
        "-p", "--prompt",
        default=None,
        help="Path to prompt template file (default: prompt.md in project root)"
    )
    parser.add_argument(
        "-m", "--model",
        default="gemini-3-pro-high",
        help="Gemini model to use (default: gemini-3-pro-high)"
    )

    args = parser.parse_args()

    try:
        analyze_paper(
            pdf_path=args.pdf,
            output_path=args.output,
            prompt_path=args.prompt,
            model=args.model
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
