# LLM Batch Processor
# Batch scoring, deduplication, and ad filtering using LLM
import json
import re
from typing import List, Dict, Any


class LLMBatchProcessor:
    """LLM 批量打分、去重、广告过滤"""

    MAX_INPUT_TOKENS = 100_000
    TARGET_BATCH_SIZE = 30

    def __init__(self, client):
        """
        Initialize the batch processor.

        Args:
            client: LLM client instance (e.g., GeminiClient)
        """
        from prompts.scoring import ScoringPrompt
        self.client = client
        self.prompt = ScoringPrompt()

    def process(self, articles: List[Dict]) -> List[Dict]:
        """
        批量处理文章

        Args:
            articles: List of article dictionaries with title, summary, tags, etc.

        Returns:
            Processed list with scores, deduplication info, ads filtered
        """
        if not articles:
            return []

        print(f"  🤖 LLM 批量处理: {len(articles)} 篇文章")

        # 分批处理
        batches = self._split_into_batches(articles)
        all_processed = []
        total_ads = 0
        total_duplicates = 0

        for i, batch in enumerate(batches, 1):
            print(f"    [{i}/{len(batches)}] 处理批次: {len(batch)} 篇...")
            result = self._process_batch(batch)
            all_processed.extend(result['articles'])

            # 统计
            total_ads += result.get('removed_ads', 0)
            total_duplicates += result.get('duplicate_groups', 0)

        # 跨批次去重（如果有多批次）
        if len(batches) > 1:
            print(f"    🔗 跨批次去重...")
            all_processed = self._cross_batch_deduplicate(all_processed)

        print(f"  ✅ LLM 处理完成: 保留 {len(all_processed)}/{len(articles)} 篇")
        if total_ads > 0:
            print(f"     🚫 过滤广告: {total_ads} 篇")
        if total_duplicates > 0:
            print(f"     🔄 去重分组: {total_duplicates} 组")

        return all_processed

    def _split_into_batches(self, articles: List[Dict]) -> List[List[Dict]]:
        """
        按 token 限制分批

        Args:
            articles: List of articles to split

        Returns:
            List of batches
        """
        batch_size = self.TARGET_BATCH_SIZE
        batches = []

        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            if batch:
                batches.append(batch)

        return batches

    def _process_batch(self, batch: List[Dict]) -> Dict[str, Any]:
        """
        处理单个批次

        Args:
            batch: List of articles in this batch

        Returns:
            Result dict with articles, removed_ads, duplicate_groups
        """
        prompt = self.prompt.format_prompt_with_articles(batch)
        response = self.client.generate_content(prompt)

        try:
            parsed = self._parse_response(response.text, batch)
            return parsed
        except Exception as e:
            print(f"      ⚠️ LLM 解析失败: {e}，使用原数据")
            # 降级：返回所有文章，标记为未处理
            return {
                'articles': batch,
                'removed_ads': 0,
                'duplicate_groups': 0
            }

    def _parse_response(self, response_text: str, original: List[Dict]) -> Dict[str, Any]:
        """
        解析 LLM 响应

        Args:
            response_text: Raw LLM response
            original: Original articles list (for reference by id)

        Returns:
            Parsed result dict
        """
        result = self._extract_json_from_response(response_text)

        processed = []
        removed_ads = 0
        duplicate_groups = 0
        seen_groups = set()

        articles_data = result.get('articles', [])

        for item in articles_data:
            article_id = item.get('id')
            if article_id is None or article_id >= len(original):
                continue

            is_ad = item.get('is_ad', False)
            keep = item.get('keep', True)
            duplicate_group = item.get('duplicate_group')

            # 统计
            if is_ad:
                removed_ads += 1
            if duplicate_group is not None and duplicate_group not in seen_groups:
                seen_groups.add(duplicate_group)
                duplicate_groups += 1

            # 跳过广告和被过滤的文章
            if not keep:
                continue

            # 更新文章数据
            article = original[article_id].copy()
            article.update({
                'score': item.get('score', 3),
                'duplicate_group': duplicate_group,
                'keep_reason': item.get('keep_reason', ''),
                'llm_processed': True
            })
            processed.append(article)

        return {
            'articles': processed,
            'removed_ads': removed_ads,
            'duplicate_groups': duplicate_groups
        }

    def _extract_json_from_response(self, text: str) -> Dict:
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

    def _cross_batch_deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        跨批次去重：基于 duplicate_group 和标题相似度

        Args:
            articles: List of processed articles from multiple batches

        Returns:
            Deduplicated list
        """
        if not articles:
            return articles

        # 按 duplicate_group 分组
        groups = {}
        ungrouped = []

        for article in articles:
            group_id = article.get('duplicate_group')
            if group_id is not None:
                if group_id not in groups:
                    groups[group_id] = []
                groups[group_id].append(article)
            else:
                ungrouped.append(article)

        # 每组只保留最高分的
        result = []
        for group_id, group_articles in groups.items():
            # 按分数降序排序
            sorted_articles = sorted(
                group_articles,
                key=lambda x: x.get('score', 0),
                reverse=True
            )
            # 保留最高分的
            best = sorted_articles[0]
            best['keep_reason'] = f"组{group_id}最优（分数{best['score']}）"
            result.append(best)

        # 添加未分组的
        result.extend(ungrouped)

        return result
