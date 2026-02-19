# Zhipu AI Client Wrapper
# OpenAI-compatible API client for GLM models
import os
import time
import requests
from typing import Optional


class ZhipuClient:
    """Zhipu AI API client with OpenAI-compatible interface."""

    API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    def __init__(
        self,
        model: str = "glm-4.7-flash",
        api_key: str = None,
        enable_thinking: bool = True,
        max_tokens: int = 65536,
    ):
        """
        Initialize Zhipu client.

        Args:
            model: Model name (default: glm-4.7-flash)
            api_key: API key for authentication (reads from ZHIPU_API_KEY env var if not provided)
            enable_thinking: Enable thinking/reasoning mode (default: True)
            max_tokens: Maximum tokens in response (default: 65536)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("ZHIPU_API_KEY")
        self.enable_thinking = enable_thinking
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError(
                "Zhipu API key is required. "
                "Set ZHIPU_API_KEY environment variable or pass api_key parameter."
            )

    def generate_content(
        self,
        prompt: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        backoff: float = 2.0,
        temperature: float = 0.7,
    ) -> "ZhipuResponse":
        """
        Generate content from text prompt with retry logic.

        Args:
            prompt: Text prompt
            max_retries: Maximum retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 2.0)
            backoff: Exponential backoff multiplier (default: 2.0)
            temperature: Sampling temperature (default: 0.7)

        Returns:
            ZhipuResponse object with .text attribute
        """
        current_delay = initial_delay
        last_exception = None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "temperature": temperature,
            "max_tokens": self.max_tokens,
        }

        # Add thinking mode if enabled
        if self.enable_thinking:
            payload["thinking"] = {"type": "enabled"}

        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    self.API_URL,
                    json=payload,
                    headers=headers,
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()
                    return ZhipuResponse(data)

                # Handle retryable status codes
                if response.status_code in [429, 500, 502, 503, 504]:
                    raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

                # Non-retryable error
                raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

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
