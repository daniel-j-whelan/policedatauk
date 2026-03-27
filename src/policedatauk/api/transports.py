"""Transport module for the policedatauk package."""

from httpx import AsyncClient, Client, HTTPStatusError, Response

from ..utils import Limiter, retry_with_backoff


class AsyncTransport:
    """Asynchronous HTTP transport class for the policedatauk package.

    Args:
        base_url (str): The base URL for the API.
        client (AsyncClient): The HTTP client.
        limiter (AsyncLimiter): The rate limiter.
    """

    def __init__(
        self, base_url: str, client: AsyncClient
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

        async with self.limiter:
            response = await self.client.request(method.upper(), url, **kwargs)

            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )

            response.raise_for_status()
            return response


class Transport:
    """Synchronous HTTP transport class for the policedatauk package.

    Args:
        base_url (str): The base URL for the API.
        client (Client): The HTTP client.
        limiter (Limiter): The rate limiter.
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

        with self.limiter:
            response = self.client.request(method.upper(), url, **kwargs)

            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )

            response.raise_for_status()
            return response
