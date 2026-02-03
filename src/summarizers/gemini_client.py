# Gemini API Client Wrapper
# Migrated from src/gemini_client.py
import google.generativeai as genai
from pathlib import Path
from typing import Optional


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

    def generate_content(self, prompt: str) -> 'genai.types.GenerateContentResponse':
        """
        Generate content from text prompt.

        Args:
            prompt: Text prompt

        Returns:
            Generation response
        """
        return self.model.generate_content(prompt)

    def analyze_pdf_bytes(
        self,
        pdf_path: str,
        prompt: str,
        pdf_data: bytes = None
    ) -> str:
        """
        Analyze a PDF file by reading it as bytes and passing to Gemini.

        Args:
            pdf_path: Path to the PDF file (for display/error message)
            prompt: Analysis prompt
            pdf_data: Optional PDF bytes data (if provided, skips file read)

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
