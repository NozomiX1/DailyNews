"""
LLM-based Deduplicator

Uses LLM to identify duplicate articles based on semantic similarity
rather than simple title matching.
"""
import json
from typing import List, Dict


class LLMDeduplicator:
    """Use LLM to deduplicate articles based on semantic similarity."""

    def __init__(self, client):
        """
        Initialize LLM deduplicator.

        Args:
            client: ZhipuClient instance
        """
        from prompts import DeduplicationPrompt
        self.client = client
        self.prompt = DeduplicationPrompt()

    def deduplicate(self, items: List[Dict], output_path: str = None) -> List[Dict]:
        """
        Deduplicate items using LLM analysis.

        Args:
            items: List of article dictionaries with title, summary, tags, etc.
            output_path: Optional path to save deduplicated JSON

        Returns:
            Deduplicated list (keeping items with smallest index for each group)
        """
        if not items:
            return []

        if len(items) <= 1:
            return items

        # Add index to each item for reference
        indexed_items = []
        for i, item in enumerate(items):
            indexed_item = {**item, '_index': i}
            indexed_items.append(indexed_item)

        # Prepare simplified data for LLM
        articles_for_llm = []
        for i, item in enumerate(items):
            article_data = {
                "index": i,
                "title": item.get("title", item.get("original_title", "")),
                "summary": item.get("summary", "")[:500],  # Truncate for context
                "tags": item.get("tags", []),
                "source": item.get("source", "")
            }
            articles_for_llm.append(article_data)

        articles_json = json.dumps(articles_for_llm, ensure_ascii=False, indent=2)

        # Call LLM to identify duplicates
        prompt = self.prompt.format_prompt(articles_json)
        try:
            response = self.client.generate_content(prompt)
            result_text = response.text.strip()

            # Parse LLM response
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                # Extract JSON from code block
                lines = result_text.split("\n")
                result_text = "\n".join(
                    line for line in lines
                    if not line.strip().startswith("```")
                )

            result = json.loads(result_text)
            duplicate_indices = set()

            if "duplicates" in result:
                for dup in result["duplicates"]:
                    idx = dup.get("index")
                    if idx is not None and idx >= 0 and idx < len(items):
                        duplicate_indices.add(idx)
                        reason = dup.get("reason", "")
                        if reason:
                            # Optionally log the reason
                            title = items[idx].get("title", "")[:50]
                            print(f"    [删除] index {idx}: {title}... ({reason})")

            # Keep items not marked as duplicates
            deduplicated = [item for i, item in enumerate(items) if i not in duplicate_indices]

            # Also remove articles with score == 1
            filtered = []
            for item in deduplicated:
                if item.get("score", 0) == 1:
                    title = item.get("title", item.get("original_title", ""))[:50]
                    print(f"    [删除] 低分文章: {title}...")
                else:
                    filtered.append(item)
            deduplicated = filtered

            # Filter out advertisements
            filtered = []
            for item in deduplicated:
                if item.get("is_ad", False):
                    title = item.get("title", item.get("original_title", ""))[:50]
                    print(f"    [删除] 广告文章: {title}...")
                else:
                    filtered.append(item)
            deduplicated = filtered

            # Save results to JSON if output_path is provided
            if output_path:
                import config
                if config.ENABLE_CACHE:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(deduplicated, f, ensure_ascii=False, indent=2)
                else:
                    print(f"      📋 无缓存模式，跳过保存 deduplicated JSON")

            return deduplicated

        except (json.JSONDecodeError, KeyError) as e:
            print(f"    ⚠️ LLM 去重解析失败: {e}")
            return items
        except Exception as e:
            print(f"    ⚠️ LLM 去重失败: {e}")
            return items
