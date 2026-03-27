"""Neighbourhood module for the policedatauk package."""

import json
from typing import Any, List, Literal, Tuple, overload

import polars as pl
from shapely.geometry import Polygon, mapping

from ...models import (
    Neighbourhood,
    NeighbourhoodResult,
    NeighbourhoodSummary,
    Person,
)
from ...utils import pydantic_to_df, validate_lat, validate_lon
from ..resources import BaseResource
from ..transports import AsyncTransport, Transport


class AsyncNeighbourhoods(BaseResource):
    """Neighbourhood-related Asynchronous API methods for the UK Police API.

    Args:
        transport (AsyncTransport): The Transport Client
    """

    def __init__(self, transport: AsyncTransport) -> None:
        """Initialise the AsyncNeighbourhoods class."""
        self.transport = transport

    @overload
    async def get_all_neighbourhoods(
        self, force: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_all_neighbourhoods(
        self, force: str, to_polars: Literal[False] = False
    ) -> List[NeighbourhoodSummary]: ...

    async def get_all_neighbourhoods(
        self,
        force: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a list of all neighbourhoods (basic summary only).
        Args:
            force: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of all neighbourhoods for a force (basic summary only).
        """
        response = await self.transport.request(
            "GET", f"/{force}/neighbourhoods"
        )
        models = self._to_model_list(response.json(), NeighbourhoodSummary)
        return self._format(models, to_polars)

    @overload
    async def get_neighbourhood(
        self, *, force: str, neighbourhood_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_neighbourhood(
        self,
        *,
        force: str,
        neighbourhood_id: str,
        to_polars: Literal[False] = False,
    ) -> Neighbourhood: ...

    async def get_neighbourhood(
        self,
        *,
        force: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific neighbourhood.
        """
        response = await self.transport.request(
            "GET", f"/{force}/{neighbourhood_id}"
        )
        model = self._to_model(response.json(), Neighbourhood)
        return self._format(model, to_polars)

    async def get_boundary(
        self, force: str, neighbourhood_id: str
    ) -> Tuple[str, Polygon]:
        """Returns the boundary of a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.

        Returns:
            A tuple containing the GeoJSON string and Shapely Polygon.
        """
        response = await self.transport.request(
            "GET", f"/{force}/{neighbourhood_id}/boundary"
        )
        boundary_data = response.json()

        coords = [
            (float(point["longitude"]), float(point["latitude"]))
            for point in boundary_data
        ]

        # Ensure polygon is closed!
        if coords and coords[0] != coords[-1]:
            coords.append(coords[0])

        polygon = Polygon(coords)

        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": neighbourhood_id},
                    "geometry": mapping(polygon),
                }
            ],
        }
        geojson_str = json.dumps(geojson)

        return geojson_str, polygon

    @overload
    async def locate_neighbourhood(
        self, *, lat: float, lon: float, to_polars: Literal[True]
    ) -> "pl.DataFrame": ...

    @overload
    async def locate_neighbourhood(
        self, *, lat: float, lon: float, to_polars: Literal[False] = False
    ) -> NeighbourhoodResult: ...

    async def locate_neighbourhood(
        self,
        *,
        lat: float,
        lon: float,
        to_polars: bool = False,
    ) -> Any:
        """Return the neighbourhood for a specific latitude and longitude.

        Args:
            lat: The latitude of the location.
            lon: The longitude of the location.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            The neighbourhood for the specific latitude and longitude.
        """
        validate_lat(lat)
        validate_lon(lon)

        params = {"q": f"{lat},{lon}"}

        response = await self.transport.request(
            "GET",
            "/locate-neighbourhood",
            params=params,
        )
        model = self._to_model(response.json(), NeighbourhoodResult)
        return self._format(model, to_polars)

    @overload
    async def get_people(
        self, *, force_id: str, neighbourhood_id: str, to_polars: Literal[True]
    ) -> "pl.DataFrame": ...

    @overload
    async def get_people(
        self,
        *,
        force_id: str,
        neighbourhood_id: str,
        to_polars: Literal[False] = False,
    ) -> List[Person]: ...

    async def get_people(
        self,
        *,
        force_id: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            People (officers) in a specific neighbourhood.
        """
        response = await self.transport.request(
            "GET", f"/{force_id}/{neighbourhood_id}/people"
        )
        models = self._to_model_list(response.json(), Person)
        return self._format(models, to_polars)

class Neighbourhoods(BaseResource):
    """Neighbourhood-related Synchronous API methods for the UK Police API.

    Args:
        transport (Transport): The Transport Client
    """

    def __init__(self, transport: Transport) -> None:
        """Initialise the AsyncNeighbourhoods class."""
        self.transport = transport

    @overload
    def get_all_neighbourhoods(
        self, force: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_all_neighbourhoods(
        self, force: str, to_polars: Literal[False] = False
    ) -> List[NeighbourhoodSummary]: ...

    def get_all_neighbourhoods(
        self,
        force: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a list of all neighbourhoods (basic summary only).
        Args:
            force: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of all neighbourhoods for a force (basic summary only).
        """
        response = self.transport.request(
            "GET", f"/{force}/neighbourhoods"
        )
        models = self._to_model_list(response.json(), NeighbourhoodSummary)
        return self._format(models, to_polars)

    @overload
    def get_neighbourhood(
        self, *, force: str, neighbourhood_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_neighbourhood(
        self,
        *,
        force: str,
        neighbourhood_id: str,
        to_polars: Literal[False] = False,
    ) -> Neighbourhood: ...

    def get_neighbourhood(
        self,
        *,
        force: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific neighbourhood.
        """
        response = self.transport.request(
            "GET", f"/{force}/{neighbourhood_id}"
        )
        model = self._to_model(response.json(), Neighbourhood)
        return self._format(model, to_polars)

    def get_boundary(
        self, force: str, neighbourhood_id: str
    ) -> Tuple[str, Polygon]:
        """Returns the boundary of a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.

        Returns:
            A tuple containing the GeoJSON string and Shapely Polygon.
        """
        response = self.transport.request(
            "GET", f"/{force}/{neighbourhood_id}/boundary"
        )
        boundary_data = response.json()

        coords = [
            (float(point["longitude"]), float(point["latitude"]))
            for point in boundary_data
        ]

        # Ensure polygon is closed!
        if coords and coords[0] != coords[-1]:
            coords.append(coords[0])

        polygon = Polygon(coords)

        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": neighbourhood_id},
                    "geometry": mapping(polygon),
                }
            ],
        }
        geojson_str = json.dumps(geojson)

        return geojson_str, polygon

    @overload
    def locate_neighbourhood(
        self, *, lat: float, lon: float, to_polars: Literal[True]
    ) -> "pl.DataFrame": ...

    @overload
    def locate_neighbourhood(
        self, *, lat: float, lon: float, to_polars: Literal[False] = False
    ) -> NeighbourhoodResult: ...

    def locate_neighbourhood(
        self,
        *,
        lat: float,
        lon: float,
        to_polars: bool = False,
    ) -> Any:
        """Return the neighbourhood for a specific latitude and longitude.

        Args:
            lat: The latitude of the location.
            lon: The longitude of the location.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            The neighbourhood for the specific latitude and longitude.
        """
        validate_lat(lat)
        validate_lon(lon)

        params = {"q": f"{lat},{lon}"}

        response = self.transport.request(
            "GET",
            "/locate-neighbourhood",
            params=params,
        )
        model = self._to_model(response.json(), NeighbourhoodResult)
        return self._format(model, to_polars)

    @overload
    def get_people(
        self, *, force_id: str, neighbourhood_id: str, to_polars: Literal[True]
    ) -> "pl.DataFrame": ...

    @overload
    def get_people(
        self,
        *,
        force_id: str,
        neighbourhood_id: str,
        to_polars: Literal[False] = False,
    ) -> List[Person]: ...

    def get_people(
        self,
        *,
        force_id: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> Any:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            People (officers) in a specific neighbourhood.
        """
        response = self.transport.request(
            "GET", f"/{force_id}/{neighbourhood_id}/people"
        )
        models = self._to_model_list(response.json(), Person)
        return self._format(models, to_polars)
