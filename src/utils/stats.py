# src/utils/stats.py
"""Statistics JSON utility for daily stats aggregation."""
import json
from pathlib import Path
from typing import Dict, Any, Optional


STATS_FILENAME = "stats.json"


def read_stats(output_dir: Path) -> Dict[str, Any]:
    """
    Read stats.json from output directory.

    Args:
        output_dir: Output directory path (e.g., output/2026-02-19/)

    Returns:
        Existing stats dict or empty dict with date
    """
    stats_path = output_dir / STATS_FILENAME
    if stats_path.exists():
        try:
            with open(stats_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Return empty structure with date from directory name
    date_str = output_dir.name
    return {"date": date_str}


def write_stats(output_dir: Path, stats: Dict[str, Any]) -> None:
    """
    Write stats.json to output directory.

    Args:
        output_dir: Output directory path
        stats: Stats dictionary to write
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    stats_path = output_dir / STATS_FILENAME

    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"  📊 Stats saved: {stats_path}")


def update_paper_stats(output_dir: Path, total_score: float, count: int) -> None:
    """
    Update paper statistics in stats.json.

    Args:
        output_dir: Output directory path
        total_score: Sum of all paper scores
        count: Number of papers
    """
    stats = read_stats(output_dir)
    stats["papers"] = {
        "total_score": round(total_score, 2),
        "count": count
    }
    write_stats(output_dir, stats)


def update_github_stats(output_dir: Path, total_stars_today: int, repo_count: int) -> None:
    """
    Update GitHub statistics in stats.json.

    Args:
        output_dir: Output directory path
        total_stars_today: Sum of today's stars for all repos
        repo_count: Number of repositories
    """
    stats = read_stats(output_dir)
    stats["github"] = {
        "total_stars_today": total_stars_today,
        "repo_count": repo_count
    }
    write_stats(output_dir, stats)
