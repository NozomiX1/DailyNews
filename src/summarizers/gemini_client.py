# Gemini API Client Wrapper
# Migrated from src/gemini_client.py
import google.generativeai as genai
import time
from pathlib import Path
from typing import Optional

try:
    from google.api_core import exceptions as gapi_exceptions
except ImportError:
    # Fallback if google.api_core is not available
    gapi_exceptions = None


class GeminiClient:
    """Unified Gemini API client with proxy support."""

    def __init__(self, model: str = "gemini-3-flash", api_key: str = None, api_endpoint: str = None):
        """
        Initialize Gemini client.

        Args:
            model: Model name to use (default: gemini-3-flash)
            api_key: API key for authentication
            api_endpoint: API endpoint URL for proxy
        """
        # Default configuration
        if api_key is None:
            api_key = 'sk-265b3049405e46928d3a7510e60fb471'
        if api_endpoint is None:
            api_endpoint = 'http://127.0.0.1:8045'

        genai.configure(
            api_key=api_key,
            transport='rest',
            client_options={'api_endpoint': api_endpoint}
        )
        self.model = genai.GenerativeModel(model)
        self.model_name = model

    def generate_content(
        self,
        prompt: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        backoff: float = 2.0
    ) -> 'genai.types.GenerateContentResponse':
        """
        Generate content from text prompt with retry logic.

        Args:
            prompt: Text prompt
            max_retries: Maximum retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 2.0)
            backoff: Exponential backoff multiplier (default: 2.0)

        Returns:
            Generation response
        """
        current_delay = initial_delay
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                last_exception = e
                error_str = str(e)

                # Check if error is retryable
                is_retryable = self._is_retryable_error(e, error_str)

                if not is_retryable or attempt >= max_retries:
                    if attempt >= max_retries and is_retryable:
                        print(f"      ⚠️ LLM请求失败，达到最大重试次数 ({max_retries})")
                    raise

                print(f"      ⚠️ LLM请求失败，{current_delay:.1f}秒后重试 ({attempt + 1}/{max_retries}): {error_str[:60]}...")
                time.sleep(current_delay)
                current_delay *= backoff

        raise last_exception

    def _is_retryable_error(self, error: Exception, error_str: str) -> bool:
        """
        Check if an error is retryable.

        Args:
            error: The exception object
            error_str: String representation of the error

        Returns:
            True if the error should be retried
        """
        # Check for specific API exception types
        if gapi_exceptions:
            if isinstance(error, (
                gapi_exceptions.ResourceExhausted,    # 429
                gapi_exceptions.ServiceUnavailable,   # 503
                gapi_exceptions.InternalServerError,   # 500
                gapi_exceptions.BadGateway,           # 502
                gapi_exceptions.GatewayTimeout,       # 504
            )):
                return True

        # Check error message for status codes (especially for proxied APIs)
        retryable_keywords = [
            '429',  # Rate limit / Resource exhausted
            '500',  # Internal server error
            '502',  # Bad gateway
            '503',  # Service unavailable
            '504',  # Gateway timeout
            'Resource has been exhausted',
            'RESOURCE_EXHAUSTED',
            'quota',
            'rate limit',
            'ConnectionError',
            'Timeout',
            'network',
        ]

        error_str_lower = error_str.lower()
        for keyword in retryable_keywords:
            if keyword.lower() in error_str_lower:
                return True

        return False

    def analyze_pdf_bytes(
        self,
        pdf_path: str,
        prompt: str,
        pdf_data: bytes = None,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        backoff: float = 2.0
    ) -> str:
        """
        Analyze a PDF file by reading it as bytes and passing to Gemini.

        Args:
            pdf_path: Path to the PDF file (for display/error message)
            prompt: Analysis prompt
            pdf_data: Optional PDF bytes data (if provided, skips file read)
            max_retries: Maximum retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 2.0)
            backoff: Exponential backoff multiplier (default: 2.0)

        Returns:
            The model's response text
        """
        if pdf_data is None:
            pdf_file = Path(pdf_path)
            if not pdf_file.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            print(f"  📄 Reading {pdf_file.name}...")
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
        else:
            print(f"  📄 Using PDF data from memory...")

        pdf_part = {
            'inline_data': {
                'mime_type': 'application/pdf',
                'data': pdf_data
            }
        }

        print(f"  🤖 Analyzing with Gemini...")

        # Use retry logic for PDF analysis
        current_delay = initial_delay
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                response = self.model.generate_content([prompt, pdf_part])
                return response.text
            except Exception as e:
                last_exception = e
                error_str = str(e)

                # Check if error is retryable
                is_retryable = self._is_retryable_error(e, error_str)

                if not is_retryable or attempt >= max_retries:
                    if attempt >= max_retries and is_retryable:
                        print(f"      ⚠️ LLM请求失败，达到最大重试次数 ({max_retries})")
                    raise

                print(f"      ⚠️ LLM请求失败，{current_delay:.1f}秒后重试 ({attempt + 1}/{max_retries}): {error_str[:60]}...")
                time.sleep(current_delay)
                current_delay *= backoff

        raise last_exception

    def upload_and_analyze(
        self,
        pdf_path: str,
        prompt: str,
        display_name: Optional[str] = None
    ) -> str:
        """
        Analyze a PDF file (wrapper for analyze_pdf_bytes).

        Args:
            pdf_path: Path to the PDF file
            prompt: Analysis prompt
            display_name: Optional (not used in bytes mode)

        Returns:
            The model's response text
        """
        return self.analyze_pdf_bytes(pdf_path, prompt)
