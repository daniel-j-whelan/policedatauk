import httpx
from aiolimiter import AsyncLimiter


class BaseAPI:
    def __init__(self, client: httpx.AsyncClient, limiter: AsyncLimiter, base_url: str):
        self.client = client
        self.limiter = limiter
        self.base_url = base_url

    async def _throttle_get_request(self, url: str) -> httpx.Response:
        """Throttle the numebr of GET requests to avoid overwhelming the endpoint."""
        async with self.limiter:
            response = await self.client.get(url)
            if response.status_code == 429:
                raise httpx.HTTPStatusError(
                    "Rate limit exceeded (429)",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response
