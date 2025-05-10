from .base import BaseAPI
from models.crime import CrimeCategory, CrimeReport
from typing import List


class CrimeAPI(BaseAPI):
    async def get_crimes_at_location(self, lat: float, lon: float) -> List[CrimeReport]:
        async with self.limiter:
            response = await self.client.get(
                f"{self.base_url}/crimes-at-location?lat={lat}&lng={lon}"
            ) 
        data = response.json()
        return [CrimeReport(**crime) for crime in data]

    async def get_crime_categories(self) -> List[CrimeCategory]:
        """Return a list of all crime categories.
        
        Returns:
            List[CrimeCategory]: A list of all crime categories.
        """
        response = await self._throttle_get_request(f"{self.base_url}/crime-categories")
        categories_data = response.json()
        return [CrimeCategory(**category) for category in categories_data]
