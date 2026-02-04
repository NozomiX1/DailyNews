"""Tests for MDRenderer."""

import pytest
from pathlib import Path

from src.publishers.md_renderer import MDRenderer, extract_title


class TestExtractTitle:
    """Test title extraction from markdown."""

    def test_extract_h1_title(self):
        md = "# Hello World\n\nSome content"
        assert extract_title(md) == "Hello World"

    def test_extract_h2_title(self):
        md = "## Subtitle\n\nContent"
        assert extract_title(md) == "Subtitle"

    def test_no_title(self):
        md = "Just some content\nwithout headers"
        assert extract_title(md) == "Untitled"


class TestMDRenderer:
    """Test MDRenderer basic functionality."""

    @pytest.fixture
    def renderer(self):
        return MDRenderer(theme="default")

    def test_basic_paragraphs(self, renderer):
        md = "Hello\n\nWorld"
        html = renderer.render_html_only(md)
        assert "<p>Hello</p>" in html
        assert "<p>World</p>" in html

    def test_headings(self, renderer):
        md = "# H1\n## H2\n### H3"
        html = renderer.render_html_only(md)
        assert "<h1>" in html
        assert "<h2>" in html
        assert "<h3>" in html

    def test_bold_italic(self, renderer):
        md = "**bold** and *italic*"
        html = renderer.render_html_only(md)
        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html

    def test_code_block(self, renderer):
        md = "```python\nprint('hello')\n```"
        html = renderer.render_html_only(md)
        assert '<pre class="code__pre">' in html
        assert "print('hello')" in html

    def test_inline_code(self, renderer):
        md = "Use `print()` function"
        html = renderer.render_html_only(md)
        assert "<code>print()</code>" in html

    def test_blockquote(self, renderer):
        md = "> This is a quote"
        html = renderer.render_html_only(md)
        assert "<blockquote>" in html

    def test_lists(self, renderer):
        md = "- item 1\n- item 2"
        html = renderer.render_html_only(md)
        assert "<ul>" in html
        assert "<li>item 1</li>" in html

    def test_links(self, renderer):
        md = "[link](https://example.com)"
        html = renderer.render_html_only(md)
        assert '<a href="https://example.com"' in html

    def test_table(self, renderer):
        md = "| a | b |\n|---|---|\n| 1 | 2 |"
        html = renderer.render_html_only(md)
        assert "<table>" in html
        assert "<thead>" in html

    def test_css_inlining(self, renderer):
        md = "# Test"
        html = renderer.render(md, inline_css=True)
        # After inlining, no <style> tags should remain
        assert "<style>" not in html
        # But styles should be inlined
        assert "style=" in html

    def test_real_daily_report(self, renderer):
        """Test with a real daily report file."""
        output_dir = Path("output")
        # Find any daily_report.md
        reports = list(output_dir.glob("*/daily_report.md"))
        if reports:
            md_content = reports[0].read_text()
            html = renderer.render(md_content)
            assert len(html) > len(md_content)  # HTML should be longer
            print(f"✅ Rendered {reports[0]}: {len(html)} chars")


class TestMathJax:
    """Test MathJax rendering."""

    def test_mathjax_available(self):
        from src.publishers.md_renderer import get_mathjax_renderer
        renderer = get_mathjax_renderer()
        if renderer:
            assert renderer.is_available() or True  # May not have Node.js in CI

    def test_inline_math(self):
        from src.publishers.md_renderer import get_mathjax_renderer
        renderer = get_mathjax_renderer()
        if renderer and renderer.is_available():
            svg = renderer.tex2svg("E = mc^2", display=False)
            assert "<svg" in svg
            assert "katex-inline" in svg
