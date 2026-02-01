# Base Publisher Class
# Abstract base class for all publishers
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class BasePublisher(ABC):
    """Abstract base class for content publishers."""

    def __init__(self):
        """Initialize the publisher."""
        pass

    @abstractmethod
    def publish(self, content: str, title: str, **kwargs) -> Dict[str, Any]:
        """
        Publish content to the target platform.

        Args:
            content: Content to publish (usually HTML or Markdown)
            title: Title for the content
            **kwargs: Additional platform-specific parameters

        Returns:
            Result dictionary with status and metadata
        """
        pass

    def _markdown_to_html(self, markdown: str) -> str:
        """
        Convert Markdown to HTML (basic implementation).

        Args:
            markdown: Markdown content

        Returns:
            HTML content
        """
        # Basic conversion - for more complex needs, use a library
        html = markdown
        html = html.replace('\n## ', '\n<h2>').replace('\n### ', '\n<h3>')
        html = html.replace('\n', '<br>\n')
        return f'<div>{html}</div>'

    def save_preview(self, content: str, output_path: str) -> None:
        """
        Save content as a preview file.

        Args:
            content: Content to save
            output_path: Path to save the file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  💾 预览已保存: {output_path}")
