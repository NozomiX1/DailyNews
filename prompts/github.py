"""
GitHub Project Summary Prompt

Prompt for summarizing GitHub trending repositories.
"""
from .base import BasePrompt


class GithubPrompt(BasePrompt):
    """Prompt for summarizing GitHub repositories with structured analysis."""

    def get_system_prompt(self) -> str:
        return """你是一位资深的 GitHub 趋势分析师和技术猎手。你的专长是透过复杂的 README 文档，精准提炼项目的核心价值、技术壁垒和应用前景。

你的目标是将输入的 GitHub 项目信息转化为一份**结构化、高信噪比**的中文分析报告。

**核心原则**：
1. **客观准确**：技术栈和功能必须基于提供的文本，严禁幻觉或臆测。
2. **深度洞察**：不要只翻译简介，要解释"它解决了什么痛点"。
3. **格式严格**：仅返回标准的 JSON 格式字符串，**严禁**使用 markdown 代码块（如 ```json ... ```），**严禁**包含任何 JSON 之外的开头或结尾文本。"""

    def get_user_prompt_template(self) -> str:
        return """请根据以下提供的 GitHub 项目信息和 README 内容，生成一份 JSON 格式的分析报告。

### 项目元数据
- 名称：{name}
- 语言：{language}
- Stars：{stars} (今日新增: {today_stars})
- 描述：{description}
- 链接：{url}

### README 内容片段
{readme_content}

---

### 输出要求
请严格按照以下 JSON 结构返回数据（Key 必须保持不变）：

{{
  "name": "{name}",
  "category": "项目领域（如：LLM工具/Web框架/DevOps/学习资料/其它）",
  "summary": "150字以内的中文深度摘要。结构建议：1. 这是一个什么项目？ 2. 解决了什么具体痛点？ 3. 核心优势是什么？",
  "tech_stack": ["关键技术1", "关键技术2"], // 仅提取最核心的语言、框架或库（最多5个）
  "use_cases": ["场景1", "场景2"], // 用户会在什么情况下使用它？
  "highlights": ["亮点1", "亮点2"], // 项目的杀手级功能或独特之处（简短）
  "is_worthy": true, // 判断逻辑：Stars增长快 OR 文档完善 OR 解决了真实痛点 OR 业界关注度高
  "recommendation_reason": "一句话推荐语（如果 is_worthy 为 false，则留空）"
}}

**再次提醒：只返回纯 JSON 字符串，不要包含 Markdown 格式标记。**"""

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
