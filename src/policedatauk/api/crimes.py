"""Crimes module for the policedatauk package."""

from typing import List

from ..models import CrimeCategory, CrimeReport, CrimeWithOutcomes
from ..utils import (
    buffer_point,
    get_last_month,
    parse_polygon,
    validate_date,
    validate_lat,
    validate_lon,
)
from .base import BaseAPI


class CrimeAPI(BaseAPI):
    """Crime-related API methods for the UK Police API."""

    async def get_crimes_by_location(
        self,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
    ) -> List[CrimeReport]:
        """Return a list of crimes at a specific location.

        Args:
            lat: Latitude of the location.
                Defaults to None.

            lon: Longitude of the location.
                Defaults to None.

            radius: The radius (in meters) to buffer the location.
                Defaults to None.

            poly: A polygon to filter crimes by.
                Defaults to None.

            date: The date for which to retrieve crimes.
                Defaults to None, which retrieves the latest month.

        Returns:
            A list of crime reports for the specified location.
        """
        params = {}
        if not poly and not (lat and lon):
            raise ValueError(
                "Either 'poly' or both 'lat' and 'lon' must be provided."
            )

        if lat and lon:
            validate_lat(lat)
            validate_lon(lon)
            if radius:
                poly = buffer_point(lat, lon, radius)
            else:
                poly = buffer_point(lat, lon, 1000)  # Default 1000m buffer

        parsed_poly = parse_polygon(poly)

        if date:
            validate_date(date)
        else:
            date = get_last_month()
        params["date"] = date
        params["poly"] = parsed_poly
        response = await self._throttle_post_request(
            f"{self.base_url}/crimes-street/all-crime", params=params
        )
        data = response.json()
        return [CrimeReport(**crime) for crime in data]

    async def get_crimes_no_location(
        self,
        force: str,
        date: str | None = None,
        category: str | None = None,
    ) -> List[CrimeReport]:
        """Return a list of crimes without a specific location.

        Args:
            force: The police force to filter crimes by.

            category: The crime category to filter by.
                Defaults to None, which retrieves all categories.

            date: The date for which to retrieve crimes.
                Defaults to None, which retrieves all crimes.

        Returns:
            A list of crime reports.
        """
        params = {"force": force}
        if date:
            validate_date(date)
        else:
            date = get_last_month()
        params["date"] = date
        if category:
            params["category"] = category
        else:
            params["category"] = "all-crime"
        response = await self._throttle_post_request(
            f"{self.base_url}/crimes-no-location", params=params
        )
        data = response.json()
        return [CrimeReport(**crime) for crime in data]

    async def get_crime_by_id(self, crime_id: str) -> CrimeReport:
        """Return a specific crime report by ID.

        Args:
            crime_id: The ID of the crime report.

        Returns:
            A specific crime report.
        """
        response = await self._throttle_post_request(
            f"{self.base_url}/outcomes-for-crime/{crime_id}"
        )
        data = response.json()
        return CrimeWithOutcomes(**data)

    async def get_crime_categories(self) -> List[CrimeCategory]:
        """Return a list of all crime categories.

        Returns:
            A list of all crime categories.
        """
        response = await self._throttle_post_request(
            f"{self.base_url}/crime-categories"
        )
        categories_data = response.json()
        return [CrimeCategory(**category) for category in categories_data]
