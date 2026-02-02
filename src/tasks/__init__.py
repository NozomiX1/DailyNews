"""
DailyNews Tasks Module

Orchestrates the complete pipeline for different content types:
- WeChat articles
- GitHub Trending
- Papers summary
- Paper analysis
"""

from .base import BaseTask
from .wechat import WechatArticleTask
from .github import GithubTrendingTask
from .papers import PapersTask
from .paper_analysis import PaperAnalysisTask

__all__ = [
    "BaseTask",
    "WechatArticleTask",
    "GithubTrendingTask",
    "PapersTask",
    "PaperAnalysisTask",
]
