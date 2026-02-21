# src/summarizers/hackernews_summarizer.py
"""
Hacker News Summarizer

Summarizes HN stories using LLM.
"""
import time
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseSummarizer
from prompts.hackernews import HackerNewsPrompt


class HackerNewsSummarizer(BaseSummarizer):
    """Summarizer for Hacker News stories."""

    def __init__(self, client):
        super().__init__(client)
        self.prompt = HackerNewsPrompt()

    def _format_comments(self, comments: List[Dict]) -> str:
        """Format comments for prompt."""
        if not comments:
            return "（无评论）"

        lines = []
        for i, comment in enumerate(comments[:5], 1):  # Top 5 comments
            by = comment.get('by', 'unknown')
            text = comment.get('text', '')[:300]  # Limit comment length
            # Clean HTML tags
            import re
            text = re.sub(r'<[^>]+>', '', text)
            lines.append(f"{i}. @{by}: {text}")

        return "\n".join(lines)

    def summarize(self, story: Dict[str, Any], article_content: str = "") -> Dict[str, Any]:
        """
        Summarize a single HN story.

        Args:
            story: Story dictionary with metadata
            article_content: Crawled article content (may be empty)

        Returns:
            Summary dictionary
        """
        title = story.get('title', 'Unknown')
        category = story.get('category', 'story')
        score = story.get('score', 0)
        descendants = story.get('descendants', 0)
        comments = story.get('comments', [])

        # Format comments
        comments_text = self._format_comments(comments)

        # Format prompt
        prompt_text = self.prompt.format_prompt_for_story(
            title=title,
            category=category,
            score=score,
            comment_count=descendants,
            article_content=article_content,
            comments=comments_text
        )

        try:
            response = self.client.generate_content(prompt_text)
            result = self._extract_json_from_response(response.text)

            # Merge with story metadata
            result.update({
                'id': story.get('id'),
                'title': title,
                'category': category,
                'score': score,
                'descendants': descendants,
                'url': story.get('url', ''),
                'by': story.get('by', 'unknown'),
                'article_fetched': bool(article_content),
                'comments': comments,
            })

            return result

        except Exception as e:
            print(f"    ❌ 总结失败 ({title}): {e}")
            # Return fallback
            return {
                'id': story.get('id'),
                'title': title,
                'category': category,
                'score': score,
                'descendants': descendants,
                'url': story.get('url', ''),
                'by': story.get('by', 'unknown'),
                'summary': '',
                'key_points': [],
                'community_sentiment': '未知',
                'worth_reading': False,
                'article_fetched': bool(article_content),
                'comments': comments[:3],  # Keep some comments for fallback display
                'error': str(e)
            }

    def summarize_batch(
        self,
        stories: List[Dict[str, Any]],
        article_contents: Dict[int, str] = None,
        delay: float = 0.5,
        output_path: str = None
    ) -> List[Dict[str, Any]]:
        """
        Summarize multiple stories.

        Args:
            stories: List of story dictionaries
            article_contents: Dict mapping story ID to article content
            delay: Delay between requests
            output_path: If provided, save results incrementally

        Returns:
            List of summary dictionaries
        """
        results = []
        total = len(stories)
        article_contents = article_contents or {}

        print(f"  🤖 开始总结 {total} 个故事...")

        for i, story in enumerate(stories, 1):
            title = story.get('title', 'Unknown')
            story_id = story.get('id')
            print(f"    [{i}/{total}] {title[:40]}...")

            article_content = article_contents.get(story_id, "")
            result = self.summarize(story, article_content)
            results.append(result)

            if output_path:
                self.save_json(results, output_path)

            if i < total:
                time.sleep(delay)

        print(f"  ✅ 总结完成，{len(results)} 个故事")
        return results
