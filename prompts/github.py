"""
GitHub Project Summary Prompt

Prompt for summarizing GitHub trending repositories.
"""
from .base import BasePrompt


class GithubPrompt(BasePrompt):
    """Prompt for summarizing GitHub repositories."""

    def get_system_prompt(self) -> str:
        return """你是一位开源项目专家，擅长快速理解项目价值和特点。

你的任务是分析 GitHub 项目的 README 或描述，生成结构化摘要。

**重要要求**：
1. 必须返回纯 JSON 格式，不要包含任何其他文字
2. 摘要要突出项目的核心价值和技术亮点
3. 技术栈要准确，不要凭空猜测"""

    def get_user_prompt_template(self) -> str:
        return """请分析以下 GitHub 项目，返回 JSON 格式：

{{
  "name": "项目名称（保持原样）",
  "summary": "100-200字中文摘要：核心功能、技术特点、适用场景",
  "tech_stack": ["技术栈1", "技术栈2"],  // 从 README 中提取的主要技术
  "use_cases": ["适用场景1", "适用场景2"],  // 典型使用场景
  "is_worthy": true  // 是否值得推荐（true/false）
}}

项目信息：
名称：{name}
描述：{description}
语言：{language}
Stars：{stars}
今日新增：{today_stars}
链接：{url}

README 内容：
{readme_content}

注意：
1. 如果没有 README，仅基于描述进行判断
2. 技术栈要从实际内容中提取，不要猜测
3. 摘要要突出"为什么这个项目值得关注"

请只返回 JSON，不要包含任何解释性文字。"""

    def format_prompt_for_repo(
        self,
        name: str,
        description: str,
        language: str,
        stars: str,
        today_stars: str,
        url: str,
        readme_content: str = ""
    ) -> str:
        """
        Format prompt for a specific repository.

        Args:
            name: Repository name
            description: Repository description
            language: Programming language
            stars: Total star count
            today_stars: Stars added today
            url: Repository URL
            readme_content: README markdown content

        Returns:
            Formatted prompt string
        """
        return self.get_user_prompt_template().format(
            name=name,
            description=description or "无描述",
            language=language or "未知",
            stars=stars or "0",
            today_stars=today_stars or "0",
            url=url,
            readme_content=readme_content or "（无 README 内容）"
        )
