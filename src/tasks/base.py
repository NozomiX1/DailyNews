# BaseTask Abstract Class
# Define the standard lifecycle for all pipeline tasks
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path


class BaseTask(ABC):
    """
    Task base class, defining the standard lifecycle for all pipeline tasks.

    Each task follows the same workflow:
    1. should_skip() - Check if the task should be skipped
    2. fetch() - Fetch raw data from source
    3. summarize() - Generate summaries using LLM
    4. format() - Format to Markdown
    5. publish() - Publish to destination
    """

    name: str = "base_task"

    def __init__(self, output_dir: Path = None, project_root: Path = None):
        """
        Initialize the task.

        Args:
            output_dir: Output directory for generated files
            project_root: Project root directory
        """
        if project_root is None:
            from pathlib import Path
            project_root = Path(__file__).parent.parent.parent

        self.project_root = project_root
        self.output_dir = output_dir or project_root / "output"

    def should_skip(self, date: str) -> bool:
        """
        Check if this task should be skipped for the given date.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            True if the task should be skipped, False otherwise
        """
        return False

    @abstractmethod
    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch raw data from source.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of raw data items
        """
        pass

    @abstractmethod
    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Generate summaries from raw data.

        Args:
            items: Raw data items from fetch()
            date: Date string in YYYY-MM-DD format

        Returns:
            List of summarized items
        """
        pass

    @abstractmethod
    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format summarized items to Markdown.

        Args:
            items: Summarized items
            date: Date string in YYYY-MM-DD format

        Returns:
            Formatted Markdown content
        """
        pass

    @abstractmethod
    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish formatted content to destination.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with status, draft_id, etc.
        """
        pass

    def run(self, date: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        Execute the complete task workflow (template method).

        Args:
            date: Date string in YYYY-MM-DD format
            dry_run: If True, skip publishing phase

        Returns:
            Result dictionary with task status
        """
        result = {
            "task": self.name,
            "date": date,
            "skipped": False,
            "fetched": 0,
            "summarized": 0,
            "published": False,
            "errors": []
        }

        # Check if should skip
        if self.should_skip(date):
            result["skipped"] = True
            return result

        try:
            # Fetch phase
            items = self.fetch(date)
            result["fetched"] = len(items)

            if not items:
                return result

            # Summarize phase
            summaries = self.summarize(items, date)
            result["summarized"] = len(summaries)

            if not summaries:
                return result

            # Format phase
            content = self.format(summaries, date)

            # Publish phase
            if not dry_run:
                pub_result = self.publish(content, date)
                result["published"] = pub_result.get("status") == "success"
                result["draft_id"] = pub_result.get("draft_id")

        except Exception as e:
            result["errors"].append(str(e))

        return result

    def print_result(self, result: Dict[str, Any]) -> None:
        """
        Print task execution result in a formatted way.

        Args:
            result: Result dictionary from run()
        """
        if result["skipped"]:
            print(f"  ⏭️  跳过")
        elif result["errors"]:
            print(f"  ❌ 错误: {result['errors']}")
        else:
            print(f"  ✅ 完成: 爬取 {result['fetched']} → 总结 {result['summarized']}")
            if result.get("published"):
                draft_id = result.get("draft_id", "")
                print(f"     📤 草稿 ID: {draft_id}")
