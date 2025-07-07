from httpx import AsyncClient, HTTPStatusError, Response
from aiolimiter import AsyncLimiter


class BaseAPI:
    def __init__(self, client: AsyncClient, limiter: AsyncLimiter, base_url: str):
        self.client = client
        self.limiter = limiter
        self.base_url = base_url

    async def _throttle_get_request(self, url: str) -> Response:
        """Perform a GET request with rate limiting.

        Args:
            url (str): URL of the request.

        Returns:
            Response: The server response.

        Exceptions:
            HTTPStatusError: If the response status code is 429 (rate limit exceeded).
        """
        async with self.limiter:
            response = await self.client.get(url)
            if response.status_code == 429:
                raise HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response
