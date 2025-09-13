"""Transport module for the policedatauk package."""

from aiolimiter import AsyncLimiter
from httpx import AsyncClient, Client, HTTPStatusError, Response

from ..utils import Limiter, retry_with_backoff


class AsyncTransport:
    """Asynchronous HTTP transport class for the policedatauk package.

    Args:
        client (AsyncClient): The HTTP client.
        limiter (AsyncLimiter): The rate limiter.
    """

    def __init__(self, client: AsyncClient, limiter: AsyncLimiter) -> None:
        """Initialise the AsyncTransport class."""
        self.client = client
        self.limiter = limiter

    @retry_with_backoff()
    async def get(self, url: str, params: dict | None = None) -> Response:
        """An asynchronous GET request with rate limiting.

        Args:
            url: The URL of the request.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        async with self.limiter:
            response = await self.client.get(url, params=params)
            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response

    @retry_with_backoff()
    async def post(
        self, url: str, json: dict | None = None, data: dict | None = None
    ) -> Response:
        """An asynchronous POST request with rate limiting.

        Args:
            url: The URL of the request.
            json: The JSON data for the POST request.
                Defaults to None.
            data: The form-encoded data for the POST request.
                Defaults to None.

        Returns:
            The server response.
        """
        async with self.limiter:
            if json:
                response = await self.client.post(url, json=json)
            elif data:
                response = await self.client.post(url, data=data)
            else:
                response = await self.client.post(url)
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
        client (Client): The HTTP client.
        limiter (Limiter): The rate limiter.
    """

    def __init__(self, client: Client, limiter: Limiter) -> None:
        """Initialise the Transport class."""
        self.client = client
        self.limiter = limiter

    @retry_with_backoff()
    def get(self, url: str, params: dict | None = None) -> Response:
        """A synchronous GET request with rate limiting.

        Args:
            url: The URL of the request.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        with self.limiter:
            response = self.client.get(url, params=params)
            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded", response.request, response
                )
            response.raise_for_status()
            return response

    @retry_with_backoff()
    def post(
        self, url: str, json: dict | None = None, data: dict | None = None
    ) -> Response:
        """A synchronous POST request with rate limiting.

        Args:
            url: The URL of the request.
            json: The JSON data for the POST request.
                Defaults to None.
            data: The form-encoded data for the POST request.
                Defaults to None.

        Returns:
            The server response.
        """
        with self.limiter:
            if json:
                response = self.client.post(url, json=json)
            elif data:
                response = self.client.post(url, data=data)
            else:
                response = self.client.post(url)
            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded", response.request, response
                )
            response.raise_for_status()
            return response
