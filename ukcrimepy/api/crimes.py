from .base import BaseAPI
from models.crime import CrimeCategory, CrimeReport
from typing import List


class CrimeAPI(BaseAPI):
    async def get_crimes_at_location(
        self, lat: float, lon: float, date: str | None = None
    ) -> List[CrimeReport]:
        """Get crimes at a specific location.

        Args:
            lat: Latitude of the location.

            lon: Longitude of the location.

            date: Date to filter crimes by (YYYY-MM).
                Defaults to None.

        Returns:
            A list of crime reports for the specified location.
        """
        params={"date": date, "lat": lat, "lng": lon}
        response = await self._throttle_get_request(
            f"{self.base_url}/crimes-at-location",
            params=params
        )
        data = response.json()
        return [CrimeReport(**crime) for crime in data]


    async def get_crimes_no_location(
        self,
        date: str | None = None,
        force: str | None = None,
        category: str | None = None
    ) -> List[CrimeReport]:
        """Return a list of crimes without a specific location.

        Args:
            date: The date for which to retrieve crimes.
                Defaults to None, which retrieves all crimes.

            force: The police force to filter crimes by.
                Defaults to None, which retrieves crimes from all forces.

            category: The crime category to filter by.
                Defaults to None, which retrieves all categories.

        Returns:
            A list of crime reports.
        """
        params = {"date": date, "force": force, "category": category}
        response = await self._throttle_get_request(
            f"{self.base_url}/crimes-no-location",
            params=params
        )
        data = response.json()
        return [CrimeReport(**crime) for crime in data]
    
    async def get_crime_categories(self) -> List[CrimeCategory]:
        """Return a list of all crime categories.

        Returns:
            A list of all crime categories.
        """
        response = await self._throttle_get_request(f"{self.base_url}/crime-categories")
        categories_data = response.json()
        return [CrimeCategory(**category) for category in categories_data]
