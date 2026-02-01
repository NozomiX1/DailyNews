"""
Batch Scoring Prompt

Prompt for batch scoring, deduplication, and ad filtering of articles.
"""
from .base import BasePrompt


class ScoringPrompt(BasePrompt):
    """Prompt for batch scoring, deduplication, and ad filtering."""

    def get_system_prompt(self) -> str:
        return """你是一位资深的内容编辑，擅长评估新闻资讯的质量和价值。

任务：对一批 AI 行业文章批量处理
1. 广告识别：标记广告性质的软文
2. 去重分组：报道同一事件/产品的文章分组
3. 质量评分：按正态分布打 1-5 分

评分标准（正态分布）：
- 5分（~5%）：奠基性论文、颠覆性创新
- 4分（~20%）：技术原理拆解、独到见解
- 3分（~50%）：教程、评测、概念解释
- 2分（~20%）：行业动态、产品发布
- 1分（~5%）：纯标题党、无实质内容"""

    def get_user_prompt_template(self) -> str:
        return """请分析以下 {count} 篇文章，返回 JSON：

{{
  "total_count": {count},
  "removed_ads": n,
  "duplicate_groups": m,
  "articles": [
    {{
      "id": 0,
      "score": 1-5,
      "is_ad": false,
      "duplicate_group": null 或组号,
      "keep": true/false,
      "keep_reason": "原因"
    }},
    ...
  ]
}}

**文章列表**：
{articles_list}

要求：
1. 评分符合正态分布（5分约5%，4分约20%，3分约50%，2分约20%，1分约5%）
2. 同一事件的文章 duplicate_group 相同
3. 同组只保留一篇最好的（keep=true）
4. 广告 is_ad=true 且 keep=false
5. 只返回 JSON，不要包含任何解释性文字"""

    def format_prompt_with_articles(self, articles: list) -> str:
        """
        Format prompt with a list of articles.

        Args:
            articles: List of article dictionaries

        Returns:
            Formatted prompt string
        """
        articles_list = self._format_articles_list(articles)
        return self.format_prompt(count=len(articles), articles_list=articles_list)

    def _format_articles_list(self, articles: list) -> str:
        """Format articles as a numbered list for the prompt."""
        lines = []
        for i, article in enumerate(articles):
            title = article.get('title', article.get('original_title', ''))
            summary = article.get('summary', '')[:200]
            tags = article.get('tags', [])
            source = article.get('source', '')

            lines.append(f"[{i}] {title}")
            if source:
                lines.append(f"    来源: {source}")
            if tags:
                lines.append(f"    标签: {', '.join(tags)}")
            if summary:
                lines.append(f"    摘要: {summary}")
            lines.append("")  # Empty line between articles

        return "\n".join(lines)
