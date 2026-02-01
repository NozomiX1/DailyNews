# Gemini API Client Wrapper
# Requires: pip install google-generativeai
import google.generativeai as genai
from pathlib import Path
from typing import Optional


class GeminiClient:
    """Unified Gemini API client with proxy support."""

    def __init__(self, model: str = "gemini-3-pro-high"):
        """
        Initialize Gemini client with Antigravity proxy.

        Args:
            model: Model name to use (default: gemini-3-pro-high)
        """
        genai.configure(
            api_key='sk-265b3049405e46928d3a7510e60fb471',
            transport='rest',
            client_options={'api_endpoint': 'http://127.0.0.1:8045'}
        )
        self.model = genai.GenerativeModel(model)

    def analyze_pdf_bytes(
        self,
        pdf_path: str,
        prompt: str
    ) -> str:
        """
        Analyze a PDF file by reading it as bytes and passing to Gemini.

        Args:
            pdf_path: Path to the PDF file
            prompt: Analysis prompt

        Returns:
            The model's response text

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: For API-related errors
        """
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print(f"Reading {pdf_file.name}...")
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        # Create a Part with the PDF data
        pdf_part = {
            'inline_data': {
                'mime_type': 'application/pdf',
                'data': pdf_data
            }
        }

        print("Analyzing with Gemini...")
        response = self.model.generate_content([prompt, pdf_part])

        return response.text

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


if __name__ == "__main__":
    # Test the client
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.gemini_client <pdf_path>")
        sys.exit(1)

    client = GeminiClient()
    result = client.upload_and_analyze(
        sys.argv[1],
        "请用中文总结这篇论文的核心贡献和创新点。"
    )
    print(result)
