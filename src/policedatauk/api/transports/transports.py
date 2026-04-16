"""Transport module for the policedatauk package."""

from httpx import (
    AsyncClient,
    Client,
    HTTPStatusError,
    RequestError,
    Response,
    TimeoutException,
)
from pyrate_limiter import Limiter

from ...exceptions import (
    NetworkError,
    RateLimitError,
    handle_exceptions,
)
from ...utils import retry_with_backoff


class AsyncTransport:
    """Asynchronous HTTP transport class for the policedatauk package.

    Args:
        base_url: The base URL for the API.
        client: The HTTP client.
        limiter: The rate limiter.
    """

    def __init__(
        self,
        base_url: str,
        client: AsyncClient,
        limiter: Limiter,
    ) -> None:
        """Initialise the AsyncTransport class."""
        self.base_url = base_url
        self.client = client
        self.limiter = limiter

    def build_url(self, endpoint: str | None) -> str:
        """Construct the full URL for a request.

        Args:
            endpoint: The endpoint of the request.
                Defaults to None.

        Returns:
            The full URL for the request.
        """
        return f"{self.base_url}{endpoint or ''}"

    @retry_with_backoff()
    async def request(
        self,
        method: str = "GET",
        endpoint: str | None = None,
        **kwargs,
    ) -> Response:
        """A single, unified asynchronous request handler with rate limiting.

        Args:
            method: the request type, e.g. GET, POST, DELETE etc
                Defaults to "GET".
            endpoint: The endpoint of the request.
                Defaults to None.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        url = self.build_url(endpoint)

        acquired = await self.limiter.try_acquire_async("api", timeout=60)
        if not acquired:
            raise RateLimitError(
                "Local rate limit exceeded. Request blocked before sending."
            )

        try:
            response = await self.client.request(method.upper(), url, **kwargs)
            response.raise_for_status()
            return response

        except HTTPStatusError as e:
            handle_exceptions(e)

        except (RequestError, TimeoutException) as e:
            raise NetworkError(f"Network connectivity issue: {str(e)}") from e


class Transport:
    """Synchronous HTTP transport class for the policedatauk package.

    Args:
        base_url: The base URL for the API.
        client: The HTTP client.
        limiter: The rate limiter.
    """

    def __init__(
        self, base_url: str, client: Client, limiter: Limiter
    ) -> None:
        """Initialise the Transport class."""
        self.base_url = base_url
        self.client = client
        self.limiter = limiter

    def build_url(self, endpoint: str | None) -> str:
        """Construct the full URL for a request.

        Args:
            endpoint: The endpoint of the request.
                Defaults to None.

        Returns:
            The full URL for the request.
        """
        return f"{self.base_url}{endpoint or ''}"

    @retry_with_backoff()
    def request(
        self,
        method: str = "GET",
        endpoint: str | None = None,
        **kwargs,
    ) -> Response:
        """A single, unified synchronous request handler with rate limiting.

        Args:
            method: the request type, e.g. GET, POST, DELETE etc
                Defaults to "GET".
            endpoint: The endpoint of the request.
                Defaults to None.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        url = self.build_url(endpoint)

        acquired = self.limiter.try_acquire("api", timeout=60)
        if not acquired:
            raise RateLimitError("Local rate limit exceeded.")

        try:
            response = self.client.request(method.upper(), url, **kwargs)
            response.raise_for_status()
            return response

        except HTTPStatusError as e:
            handle_exceptions(e)

        except (RequestError, TimeoutException) as e:
            raise NetworkError(f"Network connectivity issue: {str(e)}") from e
