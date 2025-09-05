"""Neighbourhood module for the policedatauk package."""

import json
from typing import List

from shapely.geometry import Polygon, mapping

from ..models import (
    Neighbourhood,
    NeighbourhoodResult,
    NeighbourhoodSummary,
    Person,
)
from ..utils import pydantic_to_df, validate_lat, validate_lon
from .base import BaseAPI


class NeighbourhoodAPI(BaseAPI):
    """Neighbourhood-related API methods for the UK Police API."""

    async def get_all_neighbourhoods(
        self,
        force: str,
        to_polars: bool = False,
    ) -> List[NeighbourhoodSummary]:
        """Return a list of all neighbourhoods (basic summary only).
        Args:
            force: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of all neighbourhoods for a force (basic summary only).
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/{force}/neighbourhoods"
        )
        neighbourhoods_data = response.json()

        if to_polars:
            return pydantic_to_df(
                [
                    NeighbourhoodSummary(**neighbourhood)
                    for neighbourhood in neighbourhoods_data
                ]
            )

        return [
            NeighbourhoodSummary(**neighbourhood)
            for neighbourhood in neighbourhoods_data
        ]

    async def get_neighbourhood(
        self,
        force: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> Neighbourhood:
        """Return a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific neighbourhood.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/{force}/{neighbourhood_id}"
        )
        neighbourhood_data = response.json()

        if to_polars:
            return pydantic_to_df(Neighbourhood(**neighbourhood_data))

        return Neighbourhood(**neighbourhood_data)

    async def get_boundary(
        self, force: str, neighbourhood_id: str
    ) -> Neighbourhood:
        """Return the boundary of a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.

        Returns:
            A specific neighbourhood boundary in GeoJSON & Shapely format.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/{force}/{neighbourhood_id}/boundary"
        )
        boundary_data = response.json()

        coords = [
            (float(point["longitude"]), float(point["latitude"]))
            for point in boundary_data
        ]
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        # Need to push this into the geo utils segment later
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
        geojson_str = json.dumps(geojson, default=list)

        return geojson_str, polygon

    async def locate_neighbourhood(
        self,
        lat: float,
        lon: float,
        to_polars: bool = False,
    ) -> Neighbourhood:
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
        response = await self._throttle_get_request(
            f"{self.base_url}/locate-neighbourhood",
            params={"q": f"{lat},{lon}"},
        )
        neighbourhood_data = response.json()

        if to_polars:
            return pydantic_to_df(NeighbourhoodResult(**neighbourhood_data))

        return NeighbourhoodResult(**neighbourhood_data)

    async def get_people(
        self,
        force_id: str,
        neighbourhood_id: str,
        to_polars: bool = False,
    ) -> List[Person]:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A list of people (officers) in a specific neighbourhood.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/{force_id}/{neighbourhood_id}/people"
        )
        people_data = response.json()

        if to_polars:
            return pydantic_to_df([Person(**person) for person in people_data])

        return [Person(**person) for person in people_data]
