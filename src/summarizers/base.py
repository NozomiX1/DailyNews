"""
Base Summarizer Class

Abstract base class for all content summarizers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path
import json


class BaseSummarizer(ABC):
    """Abstract base class for content summarizers."""

    def __init__(self, client):
        """
        Initialize the summarizer.

        Args:
            client: LLM client instance (e.g., ZhipuClient)
        """
        self.client = client

    @abstractmethod
    def summarize(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary for a single item.

        Args:
            content: Content to summarize
            metadata: Additional metadata (title, url, etc.)

        Returns:
            Summary as a dictionary with standardized fields
        """
        pass

    @abstractmethod
    def summarize_batch(self, items: List[Dict]) -> List[Dict]:
        """
        Summarize multiple items in batch.

        Args:
            items: List of items with 'content' and metadata fields

        Returns:
            List of summary dictionaries
        """
        pass

    def save_json(self, data: List[Dict], output_path: str) -> None:
        """
        Save summaries as JSON.

        Args:
            data: List of summary dictionaries
            output_path: Path to output JSON file
        """
        import config

        if not config.ENABLE_CACHE:
            print(f"      📋 无缓存模式，跳过保存 JSON")
            return

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"  💾 已保存 JSON: {output_path}")

    @staticmethod
    def _extract_json_from_response(text: str) -> Dict:
        """
        Extract JSON from LLM response that may contain extra text.

        Args:
            text: Raw LLM response

        Returns:
            Parsed JSON dictionary
        """
        # Try direct parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        import re

        # Look for ```json ... ```
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Look for ``` ... ```
        json_match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Look for { ... }
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"无法从响应中提取有效 JSON: {text[:200]}...")
