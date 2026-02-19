# DailyNews - GitHub Trending Fetcher
# Migrated from src/github_trending.py
import json
import requests
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
from pathlib import Path

from .base import BaseFetcher
from ..utils import retry_on_request_error, retry_on_http_error
import config


class GithubTrendingFetcher(BaseFetcher):
    """GitHub Trending repository fetcher."""

    def __init__(self, data_dir: Path = None):
        super().__init__(data_dir)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    @retry_on_http_error(max_retries=3)
    def _download_readme(self, url: str, output_path: Path) -> bool:
        """下载单个README文件"""
        resp = requests.get(url, headers=self.headers, timeout=30)
        resp.raise_for_status()
        if config.ENABLE_CACHE:
            output_path.write_text(resp.text, encoding='utf-8')
        return True

    @retry_on_request_error(max_retries=3)
    def scrape_github_trending(self, since: str = 'daily', language: str = '') -> List[Dict]:
        """
        Scrape GitHub Trending data.

        Args:
            since: Time range - 'daily', 'weekly', or 'monthly'
            language: Programming language filter

        Returns:
            List of repository dictionaries
        """
        base_url = "https://github.com/trending"
        if language:
            base_url += f"/{language}"

        params = {'since': since}

        response = requests.get(base_url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []

        repo_list = soup.find_all('article', class_='Box-row')

        for item in repo_list:
            try:
                h2_tag = item.find('h2')
                a_tag = h2_tag.find('a')
                relative_url = a_tag['href']
                repo_name = relative_url.strip('/')
                repo_url = f"https://github.com{relative_url}"

                p_tag = item.find('p')
                description = p_tag.get_text(strip=True) if p_tag else ""

                lang_span = item.find('span', itemprop='programmingLanguage')
                language_used = lang_span.get_text(strip=True) if lang_span else ""

                stats_div = item.find('div', class_='f6 color-fg-muted mt-2')
                all_links = stats_div.find_all('a') if stats_div else []

                total_stars = "0"
                if len(all_links) > 0:
                    star_link = all_links[0]
                    if 'stargazers' in star_link.get('href', ''):
                        total_stars = star_link.get_text(strip=True).replace(',', '')

                stars_period = "0"
                if stats_div:
                    spans = stats_div.find_all('span')
                    for span in spans:
                        text = span.get_text(strip=True)
                        if 'stars' in text.lower():
                            stars_period = text.split()[0].replace(',', '')
                            break

                repos.append({
                    'name': repo_name,
                    'owner': repo_name.split('/')[0] if '/' in repo_name else '',
                    'url': repo_url,
                    'description': description,
                    'language': language_used,
                    'total_stars': total_stars,
                    'stars_period': stars_period
                })

            except (AttributeError, KeyError, IndexError):
                continue

        return repos

    def fetch(self, date: str = None, since: str = 'daily', language: str = '') -> List[Dict]:
        """
        Fetch GitHub Trending repositories.

        Args:
            date: Date string (not used for trending, but for consistency)
            since: Time period - 'daily', 'weekly', or 'monthly'
            language: Programming language filter

        Returns:
            List of repository dictionaries
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        print(f"📡 获取 GitHub Trending ({since})...")

        # 首先尝试从本地 JSON 加载
        repos = self._load_from_json(date, since)
        if repos:
            print(f"  ✅ 从本地加载 {len(repos)} 个热门项目")
            self._print_data_preview(repos, "GitHub Trending")
            return repos

        # 否则从网页抓取
        repos = self.scrape_github_trending(since=since, language=language)

        if not repos:
            print("  ⚠️ 未找到项目或请求失败")
            return []

        print(f"  ✅ 找到 {len(repos)} 个热门项目")

        # Add date to each repo
        for repo in repos:
            repo['date'] = date
            repo['since'] = since

        # Print data preview
        self._print_data_preview(repos, "GitHub Trending")

        return repos

    def _print_data_preview(self, items: List[Dict], title: str):
        """打印第一条数据预览"""
        if not items:
            return

        print(f"\n📋 {title} - 数据预览 (第1条):")
        print("-" * 50)

        # 打印 JSON 预览
        first_item = items[0]
        preview_json = json.dumps(
            first_item,
            ensure_ascii=False,
            indent=2
        )
        preview_lines = preview_json.split('\n')
        for line in preview_lines[:15]:  # 前15行
            print(line)
        if len(preview_lines) > 15:
            print("... (省略)")
        print("-" * 50)

    def _load_from_json(self, date: str, since: str = 'daily') -> List[Dict]:
        """Load repos from local JSON file if exists."""
        # 新路径: data/{date}/trending/
        json_path = self.data_dir / date / "trending" / f"{date}.json"
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    repos = json.load(f)
                return repos
            except Exception as e:
                print(f"  ⚠️ 加载 JSON 失败: {e}")
        return None

    def save_raw_data(self, items: List[Dict], date: str, since: str = 'daily') -> Path:
        """Save trending data to JSON cache."""
        if not config.ENABLE_CACHE:
            print(f"      📋 无缓存模式，跳过保存 trending JSON")
            return None

        # 新路径: data/{date}/trending/
        dir_path = self.data_dir / date / "trending"
        dir_path.mkdir(parents=True, exist_ok=True)

        json_path = dir_path / f"{date}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        return json_path

    def download_readmes(self, repos: List[Dict], date: str = None) -> Dict[str, int]:
        """
        下载所有仓库的 README 文件

        Args:
            repos: 仓库列表，每个包含 'name' 字段 (格式 'owner/repo')
            date: 日期字符串，用于确定保存路径

        Returns:
            下载统计字典 {'success': 成功数, 'skipped': 跳过数, 'failed': 失败数}
        """
        if not config.ENABLE_CACHE:
            print(f"      📋 无缓存模式，跳过下载 README")
            return {'success': 0, 'skipped': len(repos), 'failed': 0}

        # 新路径: data/{date}/trending/readme_files/
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')
        readme_dir = self.data_dir / date / "trending" / "readme_files"
        readme_dir.mkdir(parents=True, exist_ok=True)

        stats = {'success': 0, 'skipped': 0, 'failed': 0}

        print(f"  📦 开始下载 {len(repos)} 个 README...")

        for repo in repos:
            name = repo.get('name', '')
            if '/' not in name:
                continue

            owner, repo_name = name.split('/', 1)

            # 扁平文件名: owner_repo.md
            filename = f"{owner}_{repo_name}.md"
            output_path = readme_dir / filename

            # 检查是否已存在
            if output_path.exists():
                stats['skipped'] += 1
                continue

            # 尝试下载
            patterns = [
                ('main', 'README.md'),
                ('master', 'README.md'),
                ('main', 'readme.md'),
                ('main', 'README.rst'),
            ]

            downloaded = False
            for branch, readme_filename in patterns:
                url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{readme_filename}"
                try:
                    # 先检查文件是否存在（不重试）
                    resp = requests.head(url, headers=self.headers, timeout=10)
                    if resp.status_code == 200:
                        # 下载内容（带重试）
                        self._download_readme(url, output_path)
                        stats['success'] += 1
                        downloaded = True
                        break
                except requests.exceptions.RequestException:
                    continue

            if not downloaded:
                stats['failed'] += 1

        print(f"    ✓ 成功: {stats['success']}, ⊙ 跳过: {stats['skipped']}, ✗ 失败: {stats['failed']}")
        return stats
