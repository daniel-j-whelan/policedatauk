from .base import BaseAPI
from models.crime import CrimeCategory, CrimeReport
from typing import List


class CrimeAPI(BaseAPI):
    async def get_crimes_at_location(
        self, lat: float, lon: float, date: str | None = None
    ) -> List[CrimeReport]:
        """Get crimes at a specific location.

        Args:
            lat (float): Latitude of the location.

            lon (float): Longitude of the location.

            date (str | None, optional): Date to filter crimes by (YYYY-MM).
                Defaults to None.

        Returns:
            List[CrimeReport]: A list of crime reports for the specified location.
        """
        async with self.limiter:
            response = await self.client.get(
                f"{self.base_url}/crimes-at-location?date={date}&lat={lat}&lng={lon}"
            )
        data = response.json()
        return [CrimeReport(**crime) for crime in data]


    async def get_crimes_no_location(
        self, date: str | None = None,
        force: str | None = None,
        category: str | None = None
    ) -> List[CrimeReport]:
        """Return a list of crimes without a specific location.

        Args:
            date (str | None): The date for which to retrieve crimes.
                Defaults to None, which retrieves all crimes.

            force (str | None): The police force to filter crimes by.
                Defaults to None, which retrieves crimes from all forces.

            category (str | None): The crime category to filter by.
                Defaults to None, which retrieves all categories.

        Returns:
            List[CrimeReport]: A list of crime reports.
        """
        params = {"date": date, "force": force, "category": category}
        response = await self._throttle_get_request(f"{self.base_url}/crimes-no-location", params=params)
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
