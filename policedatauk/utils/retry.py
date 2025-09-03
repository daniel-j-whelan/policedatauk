from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from httpx import HTTPStatusError, TimeoutException


def async_retry(max_attempts=5, base_wait=1, max_wait=4):
    """Create a retry strategy for asynchronous HTTPX requests.

    This function configures and returns a retry decorator using the tenacity library.
    The retry strategy is designed to handle exceptions of types HTTPStatusError and
    TimeoutException with exponential backoff.

    Args:
        max_attempts (int): The maximum number of retry attempts. Defaults to 5.

        base_wait (float): The base wait time (in seconds) for exponential backoff. Defaults to 1.

        max_wait (float): The maximum wait time (in seconds) for exponential backoff. Defaults to 4.

    Returns:
        A tenacity.retry decorator configured with the specified retry strategy.
    """

    return retry(
        retry=retry_if_exception_type((HTTPStatusError, TimeoutException)),
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=base_wait, max=max_wait),
        reraise=True,
    )
