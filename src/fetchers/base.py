"""
Base Fetcher Class

Abstract base class for all data fetchers.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class BaseFetcher(ABC):
    """Abstract base class for data fetchers."""

    def __init__(self, data_dir: Path = None):
        """
        Initialize the fetcher.

        Args:
            data_dir: Base directory for storing raw data
        """
        if data_dir is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
        self.data_dir = Path(data_dir)

    @abstractmethod
    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch data for a specific date.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of fetched items as dictionaries
        """
        pass

    @abstractmethod
    def save_raw_data(self, items: List[Dict[str, Any]], date: str) -> Path:
        """
        Save raw fetched data to disk.

        Args:
            items: List of fetched items
            date: Date string in YYYY-MM-DD format

        Returns:
            Path to saved file
        """
        pass

    def _ensure_dir(self, dir_path: Path) -> None:
        """Create directory if it doesn't exist."""
        dir_path.mkdir(parents=True, exist_ok=True)

    def _get_date_path(self, subdir: str, date: str, filename: str) -> Path:
        """
        Get standardized path for date-based data.

        Args:
            subdir: Subdirectory name (e.g., 'articles', 'trending')
            date: Date string in YYYY-MM-DD format
            filename: Output filename

        Returns:
            Full path to the file
        """
        dir_path = self.data_dir / subdir / date
        self._ensure_dir(dir_path)
        return dir_path / filename
