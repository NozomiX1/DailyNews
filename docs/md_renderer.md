# MDRenderer - Markdown to WeChat HTML

## Overview

`MDRenderer` converts Markdown to WeChat-compatible HTML with inline CSS, replicating doocs/md's rendering behavior.

## Features

- **Full Markdown syntax**: headings, lists, tables, code blocks, etc.
- **LaTeX formulas**: Renders to SVG via MathJax
- **Inline CSS**: WeChat requires inline styles
- **doocs/md compatible**: Same visual output as doocs/md

## Usage

```python
from src.publishers.md_renderer import MDRenderer

renderer = MDRenderer(theme="default")
html = renderer.render(markdown_content)
```

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `mistune>=3.0.0` - Markdown parsing
- `premailer>=3.10.0` - CSS inlining
- `beautifulsoup4>=4.12.0` - HTML processing
- `lxml>=5.0.0` - XML processing

### 2. Install Node.js dependencies (for MathJax)

```bash
cd src/publishers/md_renderer
npm install
```

This installs:
- `mathjax@3` - LaTeX to SVG rendering

## API Reference

### MDRenderer

```python
class MDRenderer:
    def __init__(self, theme: str = 'default')

    def render(self, markdown: str, inline_css: bool = True) -> str:
        """Render Markdown to WeChat-compatible HTML."""

    def render_html_only(self, markdown: str) -> str:
        """Render Markdown to HTML without CSS inlining."""

    def extract_title(self, markdown: str) -> str:
        """Extract title from markdown."""

    def is_mathjax_available(self) -> bool:
        """Check if MathJax renderer is available."""
```

### Functions

```python
def inline_css(html: str, theme: str = 'default') -> str:
    """Inline CSS styles into HTML for WeChat compatibility."""

def extract_title(markdown: str) -> str:
    """Extract title from markdown (first # heading)."""
```

## Themes

Available themes:
- `default` - Green theme (matches WeChat brand)
- `grace` - Elegant theme (not yet implemented)
- `simple` - Minimalist theme (not yet implemented)

## LaTeX Formulas

Supported syntax:
- Inline: `$E = mc^2$`
- Block: `$$E = mc^2$$`

Formulas are rendered as SVG via MathJax and embedded directly in the HTML.

**Note**: MathJax requires Node.js to be installed on the system.

## WeChat Publishing

```python
from src.publishers.wechat import WechatPublisher

publisher = WechatPublisher()

# Publish a daily report
publisher.publish_daily_report("output/2026-02-03/daily_report.md")

# Publish GitHub trending
publisher.publish_github_trending("output/2026-02-03/github_trending.md")

# Publish papers summary
publisher.publish_papers_summary("output/2026-02-03/papers/papers_summary.md")

# Publish a single paper
publisher.publish_single_paper("output/2026-02-03/papers/papers_note_2601.12345.md")
```

## Architecture

```
src/publishers/md_renderer/
├── __init__.py           # Module exports
├── renderer.py           # Main MDRenderer class
├── mistune_plugins.py    # Custom mistune plugins
├── mathjax.py            # MathJax LaTeX → SVG renderer
├── css_inliner.py        # CSS inlining for WeChat
├── mathjax_server.js     # Node.js MathJax server
├── package.json          # Node.js dependencies
└── css/                  # CSS styles
    ├── __init__.py
    └── base.css           # Base theme styles
```

## Development

### Running Tests

```bash
pytest tests/test_md_renderer.py -v
```

### Integration Test

```bash
# Render-only test (no WeChat API call)
python scripts/test_wechat_publish.py

# Full publish test (creates WeChat draft)
python scripts/test_wechat_publish.py --publish
```

## Known Limitations

1. **MathJax SVG compatibility**: WeChat may have limited SVG support. Consider converting SVG to PNG for production use.

2. **Theme support**: Currently only the `default` theme is fully implemented.

3. **Code highlighting**: No syntax highlighting - code blocks are styled but not colored.
