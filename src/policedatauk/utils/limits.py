"""Utilities for limiting HTTPX requests."""

import threading
import time
from types import TracebackType
from typing import Self, Type


class Limiter:
    """A rate limiter for synchronous requests.

    Args:
        burst_size: max number of burstable tokens
        refill_rate: normal tokens per second
    """

    def __init__(self, burst_size: int, refill_rate: float) -> None:
        """Initialise the Limiter class."""
        self.burst_size = float(burst_size)
        self._tokens = float(burst_size)
        self.refill_rate = float(refill_rate)
        self._last = time.monotonic()
        self._condition = threading.Condition()

    # enter and exit allow use as a context manager (e.g. with self.limiter:)
    def __enter__(self) -> Self:
        """Enter context manager.

        Returns:
            self
        """
        self.acquire()
        return self

    def __exit__(
        self,
        exception_type: Type[BaseException] | None,
        exception_value: BaseException | None,
        exception_trackback: TracebackType | None,
    ) -> bool | None:
        """Exit context manager.

        Args:
            exception_type: Type of exception
            exception_value: Value of exception
            exception_trackback: Traceback of exception

        Returns:
            False
        """
        # we don’t want to suppress exceptions from inside the with-block
        return False

    def _refill(self) -> None:
        """Refill tokens over time."""
        now = time.monotonic()
        elapsed = now - self._last
        if elapsed <= 0:
            return
        self._last = now
        self._tokens = min(
            self.burst_size, self._tokens + elapsed * self.refill_rate
        )

    def acquire(
        self, tokens: float = 1.0, timeout_s: float | None = None
    ) -> bool:
        """Blocks queries until `tokens` are acquired or timeout expires.

        Args:
            tokens: number of tokens to acquire
            timeout: maximum time to wait (seconds)

        Returns:
            True if acquired
            False if timed out
        """
        end_time = None if timeout_s is None else time.monotonic() + timeout_s

        with self._condition:
            while True:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True

                # if not enough tokens, compute wait time for next token
                needed = tokens - self._tokens
                wait_time = (
                    needed / self.refill_rate if self.refill_rate > 0 else None
                )

                if end_time is not None:
                    remaining = end_time - time.monotonic()
                    if remaining <= 0:
                        return False
                    wait_time = (
                        min(wait_time, remaining)
                        if wait_time is not None
                        else remaining
                    )

                # wait but wake up to recalc refill
                self._condition.wait(timeout=wait_time)
