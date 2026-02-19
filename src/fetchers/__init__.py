"""
DailyNews Fetchers Module

Data fetching from various sources (WeChat, GitHub, HuggingFace, etc.).
"""

from .base import BaseFetcher
from .wechat import WechatFetcher
from .github_trending import GithubTrendingFetcher
from .papers import PapersFetcher
from .hackernews import HackerNewsFetcher

__all__ = [
    "BaseFetcher",
    "WechatFetcher",
    "GithubTrendingFetcher",
    "PapersFetcher",
    "HackerNewsFetcher",
]
