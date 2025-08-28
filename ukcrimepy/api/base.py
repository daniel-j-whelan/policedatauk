from httpx import AsyncClient, HTTPStatusError, Response
from aiolimiter import AsyncLimiter
from utils.retry import async_retry


class BaseAPI:
    def __init__(self, client: AsyncClient, limiter: AsyncLimiter, base_url: str):
        self.client = client
        self.limiter = limiter
        self.base_url = base_url

    @async_retry()
    async def _throttle_post_request(
        self, url: str, data: dict | None = None
    ) -> Response:
        """Perform a POST request with rate limiting.

        Args:
            url: URL of the request.

            data: The data to include in the POST request.
                Defaults to None.

        Returns:
            The server response.

        Exceptions:
            HTTPStatusError: If the response status code is 429 (rate limit exceeded).
        """
        headers = {"Content-Type": "application/json"}
        async with self.limiter:
            response = await self.client.post(url, json=data, headers=headers)
            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response

    @async_retry()
    async def _throttle_get_request(
        self, url: str, params: dict | None = None
    ) -> Response:
        """Perform a GET request with rate limiting.

        Args:
            url: URL of the request.

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
