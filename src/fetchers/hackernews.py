# src/fetchers/hackernews.py
"""
Hacker News Fetcher

Fetches stories and comments from HN Firebase API.
"""
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from .base import BaseFetcher


class HackerNewsFetcher(BaseFetcher):
    """
    Fetcher for Hacker News using official Firebase API.

    API endpoints:
    - topstories.json: Get top story IDs
    - item/{id}.json: Get story/comment details
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, data_dir: Path = None, timeout: int = 30):
        super().__init__(data_dir)
        self.timeout = timeout

    def fetch_top_story_ids(self, limit: int = 30) -> List[int]:
        """
        Fetch top story IDs from HN.

        Args:
            limit: Maximum number of stories to fetch

        Returns:
            List of story IDs
        """
        url = f"{self.BASE_URL}/topstories.json"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        story_ids = response.json()
        return story_ids[:limit]

    def fetch_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single item (story or comment) by ID.

        Args:
            item_id: Item ID

        Returns:
            Item dictionary or None if not found
        """
        url = f"{self.BASE_URL}/item/{item_id}.json"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        return None

    def fetch_comments(self, story: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top comments for a story.

        Args:
            story: Story dictionary with 'kids' field
            limit: Maximum comments to fetch

        Returns:
            List of comment dictionaries
        """
        kids = story.get('kids', [])
        if not kids:
            return []

        comments = []
        for kid_id in kids[:limit]:
            comment = self.fetch_item(kid_id)
            if comment and comment.get('text') and not comment.get('deleted'):
                comments.append({
                    'id': comment.get('id'),
                    'by': comment.get('by', 'unknown'),
                    'text': comment.get('text', ''),
                    'time': comment.get('time', 0),
                })

        return comments

    def categorize_story(self, story: Dict[str, Any]) -> str:
        """
        Categorize story by title or type.

        Args:
            story: Story dictionary

        Returns:
            Category string: 'story', 'ask_hn', 'show_hn', 'job', 'other'
        """
        title = story.get('title', '').lower()
        story_type = story.get('type', 'story')

        if story_type == 'job':
            return 'job'
        if title.startswith('ask hn:'):
            return 'ask_hn'
        if title.startswith('show hn:'):
            return 'show_hn'
        if story_type == 'story':
            return 'story'
        return 'other'

    def fetch(self, date: str, limit: int = 30, comments_per_story: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch top stories with comments.

        Args:
            date: Date string (YYYY-MM-DD)
            limit: Number of stories to fetch
            comments_per_story: Comments to fetch per story

        Returns:
            List of story dictionaries with comments
        """
        print(f"📡 获取 Hacker News Top {limit}...")

        # Get story IDs
        story_ids = self.fetch_top_story_ids(limit)
        print(f"  ✓ 获取 {len(story_ids)} 个故事 ID")

        # Fetch each story
        stories = []
        for i, story_id in enumerate(story_ids, 1):
            print(f"  [{i}/{len(story_ids)}] 获取故事 {story_id}...", end='\r')
            story = self.fetch_item(story_id)
            if story:
                # Add category
                story['category'] = self.categorize_story(story)
                # Fetch comments
                story['comments'] = self.fetch_comments(story, comments_per_story)
                stories.append(story)

        print(f"  ✅ 获取 {len(stories)} 个故事")
        return stories

    def save_raw_data(self, items: List[Dict[str, Any]], date: str) -> Path:
        """
        Save raw stories to JSON.

        Args:
            items: List of story dictionaries
            date: Date string

        Returns:
            Path to saved file
        """
        import config
        if not config.ENABLE_CACHE:
            return None

        dir_path = self.data_dir / date / "hackernews"
        dir_path.mkdir(parents=True, exist_ok=True)

        json_path = dir_path / "stories.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        print(f"  💾 已保存: {json_path}")
        return json_path
