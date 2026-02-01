"""
Deduplication Prompt

Prompt for identifying duplicate articles from a list of summarized articles.
"""
from .base import BasePrompt


class DeduplicationPrompt(BasePrompt):
    """Prompt for identifying duplicate articles."""

    def get_system_prompt(self) -> str:
        return """你是一位资深的内容分析师，擅长识别重复报道同一事件的文章。

你的任务是分析文章列表，找出重复报道同一事件的文章。

**判断标准**：
1. 同一产品发布/模型发布/研究突破
2. 同一公司动态/人事变动
3. 同一行业事件/政策变化
4. 结合 title、summary、tags 综合判断

**去重规则**：
- 保留 index 最小的文章
- 删除其他重复项

**重要**：必须返回纯 JSON 格式。"""

    def get_user_prompt_template(self) -> str:
        return """请分析以下文章列表，找出重复报道同一事件的文章。

判断标准：
1. 同一产品发布/研究突破/公司动态/行业事件
2. 结合 title、summary、tags 综合判断

**去重规则：保留 index 最小的文章，删除其他重复项。**

返回 JSON 格式：
{{
  "duplicates": [
    {{"index": 5, "reason": "与 index 2 重复，都报道 David Silver 离职"}},
    {{"index": 8, "reason": "与 index 3 重复，都报道 Moltbook 上线"}}
  ]
}}

文章列表：
{articles_json}

请只返回 JSON，不要包含任何解释性文字。"""

    def format_prompt(self, articles_json: str) -> str:
        """
        Format prompt with articles JSON.

        Args:
            articles_json: JSON string of articles with index, title, summary, tags

        Returns:
            Formatted prompt string
        """
        return self.get_user_prompt_template().format(articles_json=articles_json)
