"""Utilities for retrying HTTPX requests."""

from typing import Callable

from httpx import HTTPStatusError, TimeoutException
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


def async_retry(
    max_attempts: int = 5, base_wait: int = 1, max_wait: int = 4
) -> Callable:
    """Create a retry strategy for asynchronous HTTPX requests.

    Configures and returns a retry decorator using the tenacity library.
    The retry strategy handles exceptions of types HTTPStatusError and
    TimeoutException with exponential backoff.

    Args:
        max_attempts: The maximum number of retry attempts.
            Defaults to 5.
        base_wait: The base wait time (in seconds) for exponential backoff.
            Defaults to 1.
        max_wait: The maximum wait time (in seconds) for exponential backoff.
            Defaults to 4.

    Returns:
        A tenacity.retry decorator configured with specified retry strategy.
    """

    return retry(
        retry=retry_if_exception_type((HTTPStatusError, TimeoutException)),
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=base_wait, max=max_wait),
        reraise=True,
    )
