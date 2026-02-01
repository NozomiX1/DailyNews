"""
Paper Summary Prompt

Prompt for summarizing academic papers from their English summary field.
This is a lightweight version that doesn't require PDF analysis.
"""
from .base import BasePrompt


class PaperSummaryPrompt(BasePrompt):
    """Prompt for summarizing academic papers from English abstract."""

    def get_system_prompt(self) -> str:
        return """你是一位 AI 研究员，擅长解读学术论文摘要。

任务：阅读论文英文摘要，生成中文总结。

输出格式（纯 JSON，不要包含任何其他文字）：
{
  "title_zh": "中文标题",
  "summary_zh": "3-5句话中文总结，包含核心贡献、方法、结论",
  "highlights": ["亮点1", "亮点2"],
  "relevance": "high/medium/low"
}

评分标准：
- relevance: "high" (重大突破/前沿热点), "medium" (有价值/相关), "low" (小众/边缘)"""

    def get_user_prompt_template(self) -> str:
        return """请分析以下论文，返回 JSON 格式：

论文标题：{title}
组织机构：{org}
GitHub Stars：{stars}
Upvotes：{upvotes}
英文摘要：{summary}

请只返回 JSON，不要包含任何解释性文字。"""

    def format_prompt_with_paper(self, paper: dict) -> str:
        """
        Format prompt with paper metadata.

        Args:
            paper: Paper dictionary with title, organization, summary, etc.

        Returns:
            Formatted prompt string
        """
        paper_detail = paper.get('paper', {})
        title = paper.get('title', '')
        org = paper.get('organization', {}).get('fullname', '')
        stars = paper_detail.get('githubStars', 0)
        upvotes = paper_detail.get('upvotes', 0)
        summary = paper_detail.get('summary', '')

        return self.format_prompt(
            title=title,
            org=org,
            stars=stars,
            upvotes=upvotes,
            summary=summary
        )
