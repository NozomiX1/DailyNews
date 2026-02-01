"""
GitHub README Downloader

Downloads README.md files from GitHub Trending repositories.
"""
import os
import re
from datetime import datetime
from typing import List, Tuple, Optional
from pathlib import Path

import requests


# Possible README filenames and branches to try
README_PATTERNS = [
    ('main', 'README.md'),
    ('master', 'README.md'),
    ('main', 'readme.md'),
    ('main', 'README.rst'),
    ('main', 'README.txt'),
]

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
README_DIR = DATA_DIR / 'readme_files'
TRENDING_DIR = DATA_DIR / 'github_trending'


def parse_trending_md(md_file: str) -> List[Tuple[str, str]]:
    """
    Parse a GitHub Trending markdown file and extract repository list.

    :param md_file: Path to the markdown file
    :return: List of (owner, repo) tuples
    """
    repos = []

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract repo names from the markdown format:
    # ## N. owner/repo
    # **链接**: https://github.com/owner/repo
    pattern = r'\*\*链接\*\*:\s+https://github\.com/([^/]+)/([^\s/]+)'

    for match in re.finditer(pattern, content):
        owner, repo = match.groups()
        repos.append((owner, repo))

    return repos


def get_readme_url(owner: str, repo: str) -> Optional[str]:
    """
    Get the working README URL for a repository.

    Tries multiple branches and filenames.

    :param owner: Repository owner
    :param repo: Repository name
    :return: URL if README found, None otherwise
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for branch, filename in README_PATTERNS:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filename}"
        try:
            response = requests.head(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return url
        except requests.RequestException:
            continue

    return None


def download_readme(owner: str, repo: str, force: bool = False) -> bool:
    """
    Download README.md from a GitHub repository.

    :param owner: Repository owner
    :param repo: Repository name
    :param force: Overwrite existing file if True
    :return: True if download successful, False otherwise
    """
    output_path = README_DIR / owner / repo / 'README.md'

    # Check if already downloaded
    if output_path.exists() and not force:
        print(f"  ✓ {owner}/{repo} - 已存在，跳过")
        return False

    # Get the README URL
    url = get_readme_url(owner, repo)
    if not url:
        print(f"  ✗ {owner}/{repo} - 未找到 README")
        return False

    # Download the content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text
    except requests.RequestException as e:
        print(f"  ✗ {owner}/{repo} - 下载失败: {e}")
        return False

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ {owner}/{repo} - 下载成功 ({len(content)} 字节)")
    return True


def is_already_downloaded(owner: str, repo: str) -> bool:
    """Check if README has already been downloaded."""
    return (README_DIR / owner / repo / 'README.md').exists()


def download_all_from_date(date: str = None, force: bool = False) -> dict:
    """
    Download all READMEs from a specific date's trending list.

    :param date: Date string (YYYY-MM-DD) or 'today', defaults to today
    :param force: Overwrite existing files if True
    :return: Dictionary with download statistics
    """
    if date is None or date == 'today':
        date = datetime.now().strftime('%Y-%m-%d')

    md_file = TRENDING_DIR / f'{date}.md'

    if not md_file.exists():
        print(f"❌ 找不到文件: {md_file}")
        return {'success': 0, 'skipped': 0, 'failed': 0, 'not_found': 0}

    repos = parse_trending_md(str(md_file))

    if not repos:
        print(f"❌ 未从文件中解析到仓库信息")
        return {'success': 0, 'skipped': 0, 'failed': 0, 'not_found': 0}

    print(f"📦 找到 {len(repos)} 个仓库，开始下载 README...\n")

    stats = {'success': 0, 'skipped': 0, 'failed': 0, 'not_found': 0}

    for owner, repo in repos:
        if is_already_downloaded(owner, repo) and not force:
            stats['skipped'] += 1
        else:
            result = download_readme(owner, repo, force)
            if result:
                stats['success'] += 1
            else:
                # Check if it was "not found" or "download failed"
                if get_readme_url(owner, repo) is None:
                    stats['not_found'] += 1
                else:
                    stats['failed'] += 1

    return stats


def list_downloaded() -> List[Tuple[str, str]]:
    """List all downloaded repositories."""
    repos = []
    if not README_DIR.exists():
        return repos

    for owner_dir in README_DIR.iterdir():
        if owner_dir.is_dir():
            for repo_dir in owner_dir.iterdir():
                if repo_dir.is_dir():
                    readme = repo_dir / 'README.md'
                    if readme.exists():
                        repos.append((owner_dir.name, repo_dir.name))

    return sorted(repos)


def main():
    """Main entry point for CLI."""
    import argparse

    parser = argparse.ArgumentParser(description='Download GitHub READMEs from Trending')
    parser.add_argument('--date', type=str, default='today',
                        help='Date (YYYY-MM-DD) or "today", default: today')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing README files')
    parser.add_argument('--list', action='store_true',
                        help='List all downloaded repositories')

    args = parser.parse_args()

    if args.list:
        repos = list_downloaded()
        if repos:
            print(f"📚 已下载 {len(repos)} 个仓库的 README:\n")
            for owner, repo in repos:
                print(f"  - {owner}/{repo}")
        else:
            print("📚 暂无已下载的 README")
        return

    print(f"🔍 正在处理 {args.date} 的 GitHub Trending...\n")
    stats = download_all_from_date(args.date, args.force)

    print(f"\n📊 下载完成:")
    print(f"  ✓ 成功: {stats['success']}")
    print(f"  ⊙ 跳过: {stats['skipped']}")
    print(f"  ✗ 未找到 README: {stats['not_found']}")
    print(f"  ✗ 下载失败: {stats['failed']}")


if __name__ == "__main__":
    main()
