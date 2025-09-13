"""Base module for the policedatauk package."""

from httpx import HTTPStatusError, Response

from ..utils import retry_with_backoff
from .transports import AsyncTransport, Transport


class BaseAPI:
    """Base class for API interaction with rate limit & retry logic."""

    def __init__(
        self, transport: AsyncTransport | Transport, base_url: str
    ) -> None:
        """Initialise the BaseAPI class.

        Args:
            transport: The HTTP transport (sync or async).
            base_url: The base URL for the API.
        """
        self.transport = transport
        self.base_url = base_url


class BaseAsyncAPI(BaseAPI):
    """Base class for async API interaction with rate limit & retry logic."""

    @retry_with_backoff()
    async def post(
        self,
        endpoint: str,
        params: dict | None = None,
        json_mode: bool = False,
    ) -> Response:
        """Perform a POST request with rate limiting.

        Args:
            endpoint: The endpoint of the request.
            params: The data to include in the POST request.
                Defaults to None.
            json_mode: If True, send as JSON body (application/json).
                If False, send as form-encoded
                    (application/x-www-form-urlencoded).
                Defaults to False.
                - True is used for Postcodes.io API.
                - False is used for UK Police API.

        Returns:
            The server response.

        Exceptions:
            HTTPStatusError: If the response status code is 429
                (rate limit exceeded).
        """
        url = f"{self.base_url}{endpoint}"
        if json_mode:
            response = await self.transport.post(url, json=params)
        else:
            response = await self.transport.post(url, data=params)

        if response.status_code == 429:
            raise HTTPStatusError(
                "Rate limit exceeded (429)",
                request=response.request,
                response=response,
            )
        response.raise_for_status()
        return response

    @retry_with_backoff()
    async def get(self, endpoint: str, params: dict | None = None) -> Response:
        """Perform a GET request with rate limiting.

        Args:
            endpoint: The endpoint of the request.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        url = f"{self.base_url}{endpoint}"
        response = await self.transport.get(url, params=params)
        if response.status_code == 429:
            raise HTTPStatusError(
                "Rate limit exceeded (429)",
                request=response.request,
                response=response,
            )
        response.raise_for_status()
        return response


class BaseSyncAPI(BaseAPI):
    """Base class for sync API interactions with rate limit & retry logic."""

    @retry_with_backoff()
    def post(
        self,
        endpoint: str,
        params: dict | None = None,
        json_mode: bool = False,
    ) -> Response:
        """Perform a POST request with rate limiting.

        Args:
            endpoint: The endpoint of the request.
            params: The data to include in the POST request.
                Defaults to None.
            json_mode: If True, send as JSON body (application/json).
                If False, send as form-encoded
                    (application/x-www-form-urlencoded).
                Defaults to False.
                - True is used for Postcodes.io API.
                - False is used for UK Police API.

        Returns:
            The server response.

        Exceptions:
            HTTPStatusError: If the response status code is 429
                (rate limit exceeded).
        """
        url = f"{self.base_url}{endpoint}"
        if json_mode:
            response = self.transport.post(url, json=params)
        else:
            response = self.transport.post(url, data=params)

        if response.status_code == 429:
            raise HTTPStatusError(
                "Rate limit exceeded (429)",
                request=response.request,
                response=response,
            )
        response.raise_for_status()
        return response

    @retry_with_backoff()
    def get(self, endpoint: str, params: dict | None = None) -> Response:
        """Perform a GET request with rate limiting.

        Args:
            endpoint: The endpoint of the request.
            params: The query parameters for the GET request.
                Defaults to None.

        Returns:
            The server response.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.transport.get(url, params=params)
        if response.status_code == 429:
            raise HTTPStatusError(
                "Rate limit exceeded (429)",
                request=response.request,
                response=response,
            )
        response.raise_for_status()
        return response
