# Zhipu AI Client Wrapper
# Using OpenAI SDK for GLM models
import os
import time
from typing import Optional
from openai import OpenAI


class ZhipuClient:
    """Zhipu AI API client using OpenAI SDK."""

    # API 配置
    BASE_URL = "https://open.bigmodel.cn/api/coding/paas/v4"  # Coding 接口

    def __init__(
        self,
        model: str = "glm-5",
        api_key: str = None,
        base_url: str = None,
        max_tokens: int = 65536,
        enable_thinking: bool = True,
    ):
        """
        Initialize Zhipu client.

        Args:
            model: Model name (default: glm-5)
            api_key: API key for authentication (reads from ZHIPU_API_KEY env var if not provided)
            base_url: API base URL (default: standard endpoint)
            max_tokens: Maximum tokens in response (default: 65536)
            enable_thinking: Enable thinking mode (default: False)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("ZHIPU_API_KEY")
        self.base_url = base_url or self.BASE_URL
        self.max_tokens = max_tokens
        self.enable_thinking = enable_thinking

        if not self.api_key:
            raise ValueError(
                "Zhipu API key is required. "
                "Set ZHIPU_API_KEY environment variable or pass api_key parameter."
            )

        # Initialize OpenAI client
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={
                "Accept-Language": "en-US,en",
                "User-Agent": "Claude-Code/1.0",
            },
        )

    def generate_content(
        self,
        prompt: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        backoff: float = 2.0,
        temperature: float = 1.0,
    ) -> "ZhipuResponse":
        """
        Generate content from text prompt with retry logic.

        Args:
            prompt: Text prompt
            max_retries: Maximum retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 2.0)
            backoff: Exponential backoff multiplier (default: 2.0)
            temperature: Sampling temperature (default: 1.0)

        Returns:
            ZhipuResponse object with .text attribute
        """
        current_delay = initial_delay
        last_exception = None

        # Build extra parameters
        extra_body = {}
        if self.enable_thinking:
            extra_body["thinking"] = {"type": "enabled"}

        for attempt in range(max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False,
                    temperature=temperature,
                    max_tokens=self.max_tokens,
                    extra_body=extra_body if extra_body else None,
                )

                # Convert to dict format for ZhipuResponse
                data = {
                    "choices": [
                        {
                            "message": {
                                "content": response.choices[0].message.content
                            }
                        }
                    ]
                }
                return ZhipuResponse(data)

            except Exception as e:
                last_exception = e
                error_str = str(e)

                # Check if error is retryable
                is_retryable = self._is_retryable_error(error_str)

                if not is_retryable or attempt >= max_retries:
                    if attempt >= max_retries and is_retryable:
                        print(f"      ⚠️ LLM请求失败，达到最大重试次数 ({max_retries})")
                    raise

                print(f"      ⚠️ LLM请求失败，{current_delay:.1f}秒后重试 ({attempt + 1}/{max_retries}): {error_str[:60]}...")
                time.sleep(current_delay)
                current_delay *= backoff

        raise last_exception

    def _is_retryable_error(self, error_str: str) -> bool:
        """Check if an error is retryable."""
        retryable_keywords = [
            "429",
            "500",
            "502",
            "503",
            "504",
            "Resource has been exhausted",
            "RESOURCE_EXHAUSTED",
            "quota",
            "rate limit",
            "ConnectionError",
            "Timeout",
            "network",
            "RateLimitError",
        ]

        error_str_lower = error_str.lower()
        for keyword in retryable_keywords:
            if keyword.lower() in error_str_lower:
                return True

        return False


class ZhipuResponse:
    """Response wrapper that mimics Gemini's response interface."""

    def __init__(self, data: dict):
        """
        Initialize response from API data.

        Args:
            data: Raw API response dictionary
        """
        self._data = data
        self._text = None

    @property
    def text(self) -> str:
        """Get the generated text content."""
        if self._text is None:
            try:
                self._text = self._data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise ValueError(f"Invalid API response format: {e}")
        return self._text
