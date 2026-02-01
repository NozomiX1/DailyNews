"""
Base Prompt Class

Abstract base class for all prompt templates.
"""
from abc import ABC, abstractmethod


class BasePrompt(ABC):
    """Abstract base class for prompt templates."""

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for the LLM."""
        pass

    @abstractmethod
    def get_user_prompt_template(self) -> str:
        """Get the user prompt template with placeholders."""
        pass

    def format_prompt(self, **kwargs) -> str:
        """
        Format the user prompt template with provided values.

        Args:
            **kwargs: Key-value pairs to substitute into the template

        Returns:
            Formatted prompt string
        """
        try:
            return self.get_user_prompt_template().format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required placeholder for prompt formatting: {e}")

    def get_full_prompt(self, **kwargs) -> str:
        """
        Get both system and user prompts combined.

        Args:
            **kwargs: Key-value pairs for user prompt formatting

        Returns:
            Combined system and user prompts
        """
        system = self.get_system_prompt()
        user = self.format_prompt(**kwargs)
        return f"{system}\n\n{user}"
