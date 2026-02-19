# prompts/hackernews.py
"""
Hacker News Summary Prompt

Prompt for summarizing HN stories with article content and comments.
"""
from .base import BasePrompt


class HackerNewsPrompt(BasePrompt):
    """Prompt for summarizing Hacker News stories with community discussion."""

    def get_system_prompt(self) -> str:
        return """你是一位技术趋势分析师，专长是从 Hacker News 讨论中提炼核心洞察。

你的任务是将文章内容和社区讨论转化为**简洁、高价值**的中文摘要。

**核心原则**：
1. **客观准确**：基于提供的内容，严禁幻觉
2. **突出价值**：文章核心观点 + 社区热议焦点
3. **格式严格**：仅返回 JSON，无 markdown 代码块"""

    def get_user_prompt_template(self) -> str:
        return """### 故事信息
- 标题：{title}
- 分类：{category}
- 得分：{score}
- 评论数：{comment_count}

### 文章正文
{article_content}

### 精选评论
{comments}

---

请生成 JSON 摘要：
{{
  "summary": "100字以内：核心内容 + 社区热议点",
  "key_points": ["要点1", "要点2", "要点3"],
  "community_sentiment": "正面/中性/负面/混合",
  "worth_reading": true
}}

**仅返回纯 JSON，不要包含任何其他文本。**"""

    def format_prompt_for_story(
        self,
        title: str,
        category: str,
        score: int,
        comment_count: int,
        article_content: str = "",
        comments: str = ""
    ) -> str:
        """
        Format prompt for a specific HN story.

        Args:
            title: Story title
            category: Story category (story, ask_hn, show_hn, job, other)
            score: Story score/upvotes
            comment_count: Number of comments
            article_content: Article body text (may be empty if crawl failed)
            comments: Formatted comments string

        Returns:
            Formatted prompt string
        """
        return self.get_user_prompt_template().format(
            title=title,
            category=category,
            score=score,
            comment_count=comment_count,
            article_content=article_content or "（正文获取失败）",
            comments=comments or "（无评论）"
        )
