"""
Paper Summary Prompt

Prompt for summarizing academic papers from their English summary field.
This is a lightweight version that doesn't require PDF analysis.
"""
from .base import BasePrompt


class PaperSummaryPrompt(BasePrompt):
    """Prompt for summarizing academic papers from English abstract."""

    def get_system_prompt(self) -> str:
        return """你是一位精通中英文的资深 AI 学术分析师。你的任务是阅读学术论文的元数据和摘要，并生成一份高质量的中文技术简报。

### 处理原则
1. **准确性**：专业术语需保留英文或使用通用中文译名，严禁幻觉。
2. **逻辑性**：总结需符合“痛点 -> 方法 -> 效果”的逻辑闭环。
3. **格式约束**：必须输出严格合法的 JSON 格式，严禁包含 ```json 代码块标记或任何额外文本。

### 输出字段定义
- `title_zh`: 论文标题的中文翻译（信达雅）。
- `summary_zh`: 150字以内的中文总结。必须包含：研究背景/解决的问题、提出的核心方法/架构、关键实验结论。
- `highlights`: 提取 3 个核心亮点（简练的短句，如“SOTA 性能”，“提出 XXX 新架构”）。
- `keywords`: 3-5 个技术关键词（中英均可）。
- `relevance`: 综合判断论文影响力，取值为 "High", "Medium", "Low"。
    - 判定依据：GitHub Stars 数量（>1000 通常为 High）、Upvotes 数量、以及摘要中是否提及“State-of-the-art”或重大突破。

### 示例输出
{"title_zh": "...", "summary_zh": "...", "highlights": ["..."], "keywords": ["..."], "relevance": "High"}"""

    def get_user_prompt_template(self) -> str:
        return """请分析以下论文元数据：

[Title]: {title}
[Organization]: {org}
[GitHub Stars]: {stars}
[Upvotes]: {upvotes}
[Abstract]:
{summary}

请直接返回 JSON 数据。"""

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
