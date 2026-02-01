"""
DailyNews Publishers Module

Publish content to various platforms (WeChat, Web, etc.).
"""

from .base import BasePublisher
from .wechat import WechatPublisher

__all__ = [
    "BasePublisher",
    "WechatPublisher",
]
