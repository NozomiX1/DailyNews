"""
DailyNews Prompts Module

Centralized prompt management for all summarization tasks.
"""

from .base import BasePrompt
from .article import ArticlePrompt
from .github import GithubPrompt
from .paper import PaperPrompt
from .paper_summary import PaperSummaryPrompt
from .deduplication import DeduplicationPrompt
from .scoring import ScoringPrompt

__all__ = [
    "BasePrompt",
    "ArticlePrompt",
    "GithubPrompt",
    "PaperPrompt",
    "PaperSummaryPrompt",
    "DeduplicationPrompt",
    "ScoringPrompt",
]
