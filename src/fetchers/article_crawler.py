# src/fetchers/article_crawler.py
"""
Article Crawler

Uses Crawl4AI to extract article content from URLs.
"""
import asyncio
from typing import List, Dict, Any


class ArticleCrawler:
    """
    Crawl article content using Crawl4AI.

    Features:
    - Async crawling with concurrency control
    - Automatic content extraction
    - Graceful error handling
    """

    def __init__(self, timeout: int = 30, max_retries: int = 2):
        self.timeout = timeout
        self.max_retries = max_retries

    async def _crawl_single(self, url: str) -> Dict[str, Any]:
        """
        Crawl a single URL asynchronously.

        Args:
            url: URL to crawl

        Returns:
            Dict with 'success', 'content', 'error' fields
        """
        from crawl4ai import AsyncWebCrawler

        try:
            async with AsyncWebCrawler(verbose=False, headless=True) as crawler:
                result = await crawler.arun(
                    url=url,
                    word_count_threshold=50,
                    bypass_cache=True,
                )

                if result.success:
                    return {
                        'success': True,
                        'content': result.markdown[:5000],  # Limit content length
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'content': '',
                        'error': result.error_message or 'Unknown error'
                    }
        except Exception as e:
            return {
                'success': False,
                'content': '',
                'error': str(e)[:200]
            }

    async def crawl_batch_async(
        self,
        urls: List[str],
        concurrency: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Crawl multiple URLs concurrently.

        Args:
            urls: List of URLs to crawl
            concurrency: Maximum concurrent crawls

        Returns:
            List of crawl results
        """
        semaphore = asyncio.Semaphore(concurrency)

        async def crawl_with_limit(url: str) -> Dict[str, Any]:
            async with semaphore:
                return await self._crawl_single(url)

        tasks = [crawl_with_limit(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'success': False,
                    'content': '',
                    'error': str(result)[:200]
                })
            else:
                processed_results.append(result)

        return processed_results

    def crawl_batch(self, urls: List[str], concurrency: int = 5) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for batch crawling.

        Args:
            urls: List of URLs to crawl
            concurrency: Maximum concurrent crawls

        Returns:
            List of crawl results
        """
        return asyncio.run(self.crawl_batch_async(urls, concurrency))

    def crawl(self, url: str) -> Dict[str, Any]:
        """
        Crawl a single URL (synchronous).

        Args:
            url: URL to crawl

        Returns:
            Dict with 'success', 'content', 'error' fields
        """
        return asyncio.run(self._crawl_single(url))
