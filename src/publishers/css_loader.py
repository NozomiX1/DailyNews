"""
CSS 加载器 - 从 doocs/md 的 CSS 文件加载样式
"""
from pathlib import Path


def load_theme_css() -> str:
    """
    加载 doocs/md 的主题 CSS 文件

    Returns:
        合并后的 CSS 字符串（base.css + default.css）
    """
    project_root = Path(__file__).parent.parent.parent
    css_dir = project_root / "md" / "packages" / "shared" / "src" / "configs" / "theme-css"

    base_css = (css_dir / "base.css").read_text(encoding="utf-8")
    default_css = (css_dir / "default.css").read_text(encoding="utf-8")

    # 替换 CSS 变量为具体值（微信不支持 CSS 变量）
    css_variables = {
        "var(--md-primary-color)": "#1a73e8",
        "var(--md-font-family)": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "var(--md-font-size)": "15px",
        "var(--blockquote-background)": "#f7f7f7",
        "hsl(var(--foreground))": "#333",
        "calc(var(--md-font-size) * 1.2)": "18px",
        "calc(var(--md-font-size) * 1.1)": "16.5px",
        "calc(var(--md-font-size) * 1)": "15px",
    }

    combined_css = base_css + "\n" + default_css

    for var, value in css_variables.items():
        combined_css = combined_css.replace(var, value)

    return combined_css


def get_inline_styles_css() -> str:
    """
    获取用于 premailer 的 CSS

    Returns:
        处理后的 CSS 字符串
    """
    base_css = load_theme_css()

    # 添加文章列表专用的样式
    list_css = """

/* ==================== 文章列表专用样式 ==================== */
.article-list {
  font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}

.article-spacer {
  margin-top: 20px;
}

.article-title {
  margin-top: 30px;
  margin-bottom: 5px;
  font-size: 18px;
  font-weight: bold;
  color: #000;
}

.article-meta {
  font-size: 13px;
  color: #888;
  margin-bottom: 10px;
  background: #f9f9f9;
  padding: 8px;
  border-radius: 4px;
}

.article-summary {
  font-size: 16px;
  color: #333;
  line-height: 1.6;
  margin-bottom: 25px;
}

.article-link {
  display: inline-block;
  margin-top: 4px;
  color: #576b95;
  word-break: break-all;
}

.tech-stack {
  display: inline-block;
  margin-top: 4px;
  color: #666;
  font-size: 13px;
}

.highlight-box {
  font-size: 14px;
  color: #666;
  background: #f0f7ff;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 25px;
  border-left: 3px solid #3498db;
}

.highlight-box-warning {
  background: #fff8e1;
  border-left-color: #f39c12;
}

.article-divider {
  border: 0;
  border-top: 1px dashed #ddd;
  margin: 20px 0;
}
"""

    return base_css + list_css
