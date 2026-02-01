# Article Summarizer
# Summarize WeChat Official Account articles
import json
import time
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseSummarizer
from prompts.article import ArticlePrompt


class ArticleSummarizer(BaseSummarizer):
    """Summarizer for WeChat articles."""

    def __init__(self, client):
        super().__init__(client)
        self.prompt = ArticlePrompt()

    def summarize(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single article.

        Args:
            content: Article content (markdown)
            metadata: Article metadata (title, url, source, etc.)

        Returns:
            Summary dictionary with title, score, tags, summary, is_ad
        """
        title = metadata.get('title', '')
        source = metadata.get('account', metadata.get('source', ''))
        url = metadata.get('url', '')

        # Format prompt
        prompt_text = self.prompt.format_prompt_with_metadata(
            title=title,
            content=content[:10000],  # Limit content length
            source=source,
            url=url
        )

        try:
            # Call LLM
            response = self.client.generate_content(prompt_text)
            result = self._extract_json_from_response(response.text)

            # Merge with metadata
            result['source'] = source
            result['url'] = url
            result['original_title'] = title
            result['time'] = metadata.get('time_str', '')
            result['timestamp'] = metadata.get('timestamp', 0)

            # Ensure score and is_ad have default values
            if 'score' not in result:
                result['score'] = 2  # Default to 2 (fast news/briefing)
            if 'is_ad' not in result:
                result['is_ad'] = False

            return result

        except Exception as e:
            print(f"    ❌ 总结失败: {e}")
            # Return fallback result with default score
            return {
                'title': title[:50] + '...' if len(title) > 50 else title,
                'tags': ['未分类'],
                'summary': f"文章摘要生成失败。原标题：{title}",
                'score': 1,  # Default low score for errors
                'is_ad': False,
                'source': source,
                'url': url,
                'original_title': title,
                'time': metadata.get('time_str', ''),
                'timestamp': metadata.get('timestamp', 0),
                'error': str(e)
            }

    def summarize_batch(self, articles: List[Dict], delay: float = 1.0, output_path: str = None) -> List[Dict]:
        """
        Summarize multiple articles.

        Args:
            articles: List of article dicts with 'content' and metadata
            delay: Delay between requests in seconds
            output_path: If provided, save after each article (边总结边保存)

        Returns:
            List of summary dictionaries
        """
        results = []
        total = len(articles)

        print(f"  🤖 开始总结 {total} 篇文章...")

        for i, article in enumerate(articles, 1):
            title = article.get('title', article.get('original_title', ''))
            print(f"    [{i}/{total}] {title[:40]}...")

            md_content = article.get('content', '')

            if not md_content or len(md_content) < 100:
                print(f"      ⚠️ 内容过短，跳过")
                continue

            result = self.summarize(md_content, article)
            results.append(result)
            score = result.get('score', 0)
            stars = '🌟' * score if score > 0 else 'N/A'
            print(f"      ✅ 标签: {result.get('tags')} | 评分: {stars}")

            # 边总结边保存：每篇完成后立即写入
            if output_path:
                self.save_json(results, output_path)

            # Rate limiting
            if i < total:
                time.sleep(delay)

        print(f"  ✅ 总结完成，共 {len(results)} 篇")

        return results
