"""Crimes module for the policedatauk package."""

from typing import List, Literal, overload

import polars as pl

from ...models import CrimeCategory, CrimeReport, CrimeWithOutcomes
from ...utils import (
    buffer_point,
    get_last_month,
    parse_polygon,
    validate_date,
    validate_lat,
    validate_lon,
)
from ..resources import BaseResource
from ..transports import AsyncTransport, Transport


class AsyncCrimes(BaseResource):
    """Crime-related Asynchronous API methods for the UK Police API.

    Args:
        transport: The Transport Client
    """

    def __init__(self, transport: AsyncTransport) -> None:
        """Initialise the AsyncCrimes class."""
        self.transport = transport

    @overload
    async def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    async def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: Literal[False] = False,
    ) -> List[CrimeReport]: ...

    async def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeReport]:
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
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

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
        response = await self.transport.request(
            "POST", "/crimes-street/all-crime", data=params
        )
        crimes = self._to_model_list(response.json(), CrimeReport)
        return self._format(crimes, to_polars)

    @overload
    async def get_crimes_no_location(
        force: str,
        to_polars: Literal[True],
        date: str | None = None,
        category: str | None = None,
    ) -> pl.DataFrame: ...

    @overload
    async def get_crimes_no_location(
        force: str,
        date: str | None = None,
        category: str | None = None,
        to_polars: Literal[False] = False,
    ) -> List[CrimeReport]: ...

    async def get_crimes_no_location(
        self,
        force: str,
        date: str | None = None,
        category: str | None = None,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeReport]:
        """Return a list of crimes without a specific location.

        Args:
            force: The police force to filter crimes by.
            category: The crime category to filter by.
                Defaults to None, which retrieves all categories.
            date: The date for which to retrieve crimes.
                Defaults to None, which retrieves all crimes.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

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
        response = await self.transport.request(
            "POST", "/crimes-no-location", params=params
        )
        crimes = self._to_model_list(response.json(), CrimeReport)
        return self._format(crimes, to_polars)

    @overload
    async def get_crime_by_id(
        crime_id: str | int,
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    async def get_crime_by_id(
        crime_id: str | int,
        to_polars: Literal[False] = False,
    ) -> CrimeWithOutcomes: ...

    async def get_crime_by_id(
        self,
        crime_id: str | int,
        to_polars: bool = False,
    ) -> pl.DataFrame | CrimeWithOutcomes:
        """Return a specific crime report by ID.

        Args:
            crime_id: The ID of the crime report.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific crime report.
        """
        response = await self.transport.request(
            "POST", f"/outcomes-for-crime/{crime_id}"
        )
        crimes = self._to_model(response.json(), CrimeWithOutcomes)
        return self._format(crimes, to_polars)

    @overload
    async def get_crime_categories(
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    async def get_crime_categories(
        to_polars: Literal[False] = False,
    ) -> List[CrimeCategory]: ...

    async def get_crime_categories(
        self,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeCategory]:
        """Return a list of all crime categories.

        Args:
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of all crime categories.
        """
        response = await self.transport.request("POST", "crime-categories")
        categories = self._to_model_list(response.json(), CrimeCategory)
        return self._format(categories, to_polars)


class Crimes(BaseResource):
    """Crime-related Synchronous API methods for the UK Police API.

    Args:
        transport (Transport): The Transport Client
    """

    def __init__(self, transport: Transport, max_workers: int = 10) -> None:
        """Initialise the Crimes class."""
        self.transport = transport
        self.max_workers = max_workers

    @overload
    def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: Literal[False] = False,
    ) -> List[CrimeReport]: ...

    def get_crimes_by_location(
        self,
        *,
        lat: float | None = None,
        lon: float | None = None,
        radius: int | None = None,
        poly: str | None = None,
        date: str | None = None,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeReport]:
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
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

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
        response = self.transport.request(
            "POST", "/crimes-street/all-crime", data=params
        )
        crimes = self._to_model_list(response.json(), CrimeReport)
        return self._format(crimes, to_polars)

    @overload
    def get_crimes_no_location(
        force: str,
        to_polars: Literal[True],
        date: str | None = None,
        category: str | None = None,
    ) -> pl.DataFrame: ...

    @overload
    def get_crimes_no_location(
        force: str,
        date: str | None = None,
        category: str | None = None,
        to_polars: Literal[False] = False,
    ) -> List[CrimeReport]: ...

    def get_crimes_no_location(
        self,
        force: str,
        date: str | None = None,
        category: str | None = None,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeReport]:
        """Return a list of crimes without a specific location.

        Args:
            force: The police force to filter crimes by.
            category: The crime category to filter by.
                Defaults to None, which retrieves all categories.
            date: The date for which to retrieve crimes.
                Defaults to None, which retrieves all crimes.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

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
        response = self.transport.request(
            "POST", "/crimes-no-location", params=params
        )
        crimes = self._to_model_list(response.json(), CrimeReport)
        return self._format(crimes, to_polars)

    @overload
    def get_crime_by_id(
        crime_id: str | int,
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    def get_crime_by_id(
        crime_id: str | int,
        to_polars: Literal[False] = False,
    ) -> CrimeWithOutcomes: ...

    def get_crime_by_id(
        self,
        crime_id: str | int,
        to_polars: bool = False,
    ) -> pl.DataFrame | CrimeWithOutcomes:
        """Return a specific crime report by ID.

        Args:
            crime_id: The ID of the crime report.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific crime report.
        """
        response = self.transport.request(
            "POST", f"/outcomes-for-crime/{crime_id}"
        )
        crimes = self._to_model(response.json(), CrimeWithOutcomes)
        return self._format(crimes, to_polars)

    @overload
    def get_crime_categories(
        to_polars: Literal[True],
    ) -> pl.DataFrame: ...

    @overload
    def get_crime_categories(
        to_polars: Literal[False] = False,
    ) -> List[CrimeCategory]: ...

    def get_crime_categories(
        self,
        to_polars: bool = False,
    ) -> pl.DataFrame | List[CrimeCategory]:
        """Return a list of all crime categories.

        Args:
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of all crime categories.
        """
        response = self.transport.request("POST", "crime-categories")
        categories = self._to_model_list(response.json(), CrimeCategory)
        return self._format(categories, to_polars)
