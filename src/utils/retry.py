# DailyNews - Retry Decorator
# 网络请求失败重试装饰器
import time
import requests
from functools import wraps
from typing import Callable, Type, Tuple, Optional, Set


def retry_on_request_error(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ),
    retryable_statuses: Optional[Set[int]] = None
) -> Callable:
    """
    重试装饰器，用于网络请求失败时自动重试。

    Args:
        max_retries: 最大重试次数，默认3次
        delay: 初始重试延迟（秒），默认1秒
        backoff: 退避系数，每次重试延迟时间 = delay * (backoff ** retry_count)
        exceptions: 需要重试的异常类型
        retryable_statuses: 可重试的HTTP状态码集合（如 {429, 500, 502, 503, 504}）

    Returns:
        装饰后的函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # 检查是否是HTTPError且状态码不在可重试列表中
                    if isinstance(e, requests.exceptions.HTTPError) and retryable_statuses is not None:
                        if hasattr(e.response, 'status_code') and e.response.status_code not in retryable_statuses:
                            raise  # 不可重试的状态码直接抛出

                    if attempt < max_retries:
                        print(f"    ⚠️ 请求失败，{current_delay:.1f}秒后重试 ({attempt + 1}/{max_retries}): {str(e)[:50]}...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"    ❌ 达到最大重试次数 ({max_retries})，放弃")

            raise last_exception

        return wrapper
    return decorator


def retry_on_http_error(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    retryable_statuses: Set[int] = (429, 500, 502, 503, 504)
) -> Callable:
    """
    专门针对HTTP错误的重试装饰器。

    Args:
        max_retries: 最大重试次数，默认3次
        delay: 初始重试延迟（秒），默认1秒
        backoff: 退避系数
        retryable_statuses: 可重试的HTTP状态码

    Returns:
        装饰后的函数
    """
    return retry_on_request_error(
        max_retries=max_retries,
        delay=delay,
        backoff=backoff,
        exceptions=(requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        retryable_statuses=retryable_statuses
    )
