"""
GitHub Trending Scraper

Fetches trending repositories from GitHub and saves to Markdown format.
"""
import os
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


def scrape_github_trending(since: str = 'daily', language: str = '') -> List[Dict]:
    """
    Scrape GitHub Trending data.

    :param since: Time range - 'daily', 'weekly', or 'monthly'
    :param language: Programming language filter (e.g., 'python', 'javascript'), empty for all
    :return: List of repository dictionaries
    """
    base_url = "https://github.com/trending"
    if language:
        base_url += f"/{language}"

    params = {'since': since}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(base_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []

    # Each trending repository is in an article tag with class 'Box-row'
    repo_list = soup.find_all('article', class_='Box-row')

    for item in repo_list:
        try:
            # 1. Extract repo name and link
            h2_tag = item.find('h2')
            a_tag = h2_tag.find('a')
            relative_url = a_tag['href']  # e.g., /owner/repo
            repo_name = relative_url.strip('/')
            repo_url = f"https://github.com{relative_url}"

            # 2. Extract description (some repos don't have one)
            p_tag = item.find('p')
            description = p_tag.get_text(strip=True) if p_tag else ""

            # 3. Extract programming language
            lang_span = item.find('span', itemprop='programmingLanguage')
            language_used = lang_span.get_text(strip=True) if lang_span else ""

            # 4. Extract star counts (total stars and stars today/this week)
            stats_div = item.find('div', class_='f6 color-fg-muted mt-2')
            all_links = stats_div.find_all('a') if stats_div else []

            total_stars = "0"
            if len(all_links) > 0:
                star_link = all_links[0]
                if 'stargazers' in star_link.get('href', ''):
                    total_stars = star_link.get_text(strip=True).replace(',', '')

            # 5. Extract stars added today/this week
            # Text is usually like "100 stars today" or "1,234 stars this week"
            stars_period = "0"
            if stats_div:
                spans = stats_div.find_all('span')
                for span in spans:
                    text = span.get_text(strip=True)
                    if 'stars' in text.lower():
                        # Extract the number before "stars"
                        stars_period = text.split()[0].replace(',', '')
                        break

            repos.append({
                'name': repo_name,
                'url': repo_url,
                'description': description,
                'language': language_used,
                'total_stars': total_stars,
                'stars_period': stars_period
            })

        except (AttributeError, KeyError, IndexError):
            # Skip items with parsing errors
            continue

    return repos


def format_stars_count(stars_str: str) -> str:
    """Format stars count with comma separator."""
    try:
        num = int(stars_str)
        return f"{num:,}"
    except ValueError:
        return stars_str


def repos_to_markdown(repos: List[Dict], date: str = None, since: str = 'daily') -> str:
    """
    Convert repository list to Markdown format.

    :param repos: List of repository dictionaries
    :param date: Date string (YYYY-MM-DD), defaults to today
    :param since: Time period for context
    :return: Markdown formatted string
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    period_label = {
        'daily': '今日',
        'weekly': '本周',
        'monthly': '本月'
    }.get(since, '本期')

    md_lines = [
        f"# GitHub Trending | {date}",
        "",
        f"**时间范围**: {period_label}",
        f"**项目数量**: {len(repos)}",
        "",
        "---",
        ""
    ]

    for idx, repo in enumerate(repos, 1):
        md_lines.append(f"## {idx}. {repo['name']}")
        md_lines.append(f"**语言**: {repo['language'] or 'N/A'} | "
                       f"**Stars**: {format_stars_count(repo['total_stars'])} | "
                       f"**{period_label}**: +{format_stars_count(repo['stars_period'])}")
        md_lines.append(f"**链接**: {repo['url']}")
        md_lines.append("")

        if repo['description']:
            md_lines.append(f"{repo['description']}")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    return "\n".join(md_lines)


def save_to_markdown(repos: List[Dict], output_dir: str = None,
                     date: str = None, since: str = 'daily') -> str:
    """
    Save repositories to a Markdown file.

    :param repos: List of repository dictionaries
    :param output_dir: Output directory path
    :param date: Date string (YYYY-MM-DD), defaults to today
    :param since: Time period
    :return: Path to the saved file
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data', 'github_trending'
        )

    os.makedirs(output_dir, exist_ok=True)

    filename = f"{date}.md"
    filepath = os.path.join(output_dir, filename)

    markdown_content = repos_to_markdown(repos, date, since)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return filepath


def main():
    """Main entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Scrape GitHub Trending')
    parser.add_argument('--since', choices=['daily', 'weekly', 'monthly'],
                        default='daily', help='Time period')
    parser.add_argument('--language', type=str, default='',
                        help='Programming language filter')
    parser.add_argument('--output', type=str, default=None,
                        help='Output directory')
    parser.add_argument('--date', type=str, default=None,
                        help='Date (YYYY-MM-DD), default today')

    args = parser.parse_args()

    print(f"Fetching GitHub Trending ({args.since})" +
          (f" for {args.language}" if args.language else "") + "...")

    repos = scrape_github_trending(since=args.since, language=args.language)

    if not repos:
        print("No repositories found or request failed.")
        return

    print(f"Found {len(repos)} trending repositories.")

    filepath = save_to_markdown(
        repos,
        output_dir=args.output,
        date=args.date,
        since=args.since
    )

    print(f"Saved to: {filepath}")

    # Print preview
    print("\n--- Preview ---")
    for repo in repos[:3]:
        print(f"  {repo['name']} ({repo['language']}) - "
              f"+{repo['stars_period']} stars today")


if __name__ == "__main__":
    main()
