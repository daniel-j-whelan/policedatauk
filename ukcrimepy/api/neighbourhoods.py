import asyncio
from .base import BaseAPI
from models import Force, ForceSummary, Person, Neighbourhood
from typing import List


class NeighbourhoodAPI(BaseAPI):
    """Neighbourhood-related API methods for the UK Police API."""

    async def get_all_neighbourhoods(self, force: str) -> List[Neighbourhood]:
        """Return a list of all neighbourhoods (basic summary only).
        Args:
            force: The ID of the police force.

        Returns:
            A list of all neighbourhoods for a force (basic summary only).
        """
        response = await self._throttle_post_request(
            f"{self.base_url}/{force}/neighbourhoods"
        )
        neighbourhoods_data = response.json()
        return [Neighbourhood(**neighbourhood) for neighbourhood in neighbourhoods_data]

    async def get_neighbourhood(
        self, force: str, neighbourhood_id: str
    ) -> Neighbourhood:
        """Return a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.

        Returns:
            A specific neighbourhood.
        """
        response = await self._throttle_post_request(
            f"{self.base_url}/{force}/{neighbourhood_id}"
        )
        neighbourhood_data = response.json()
        return Neighbourhood(**neighbourhood_data)

    async def get_boundary(
        self, force: str, neighbourhood_id: str, to_geojson: bool = False
    ) -> Neighbourhood:
        """Return the boundary of a specific neighbourhood by ID.

        Args:
            force: The ID of the police force.
            neighbourhood_id: The ID of the neighbourhood.
            to_geojson: Whether to convert the boundary to GeoJSON format or Police API format.

        Returns:
            A neighbourhood boundary.
        """
        response = await self._throttle_post_request(
            f"{self.base_url}/{force}/{neighbourhood_id}/boundary"
        )
        boundary_data = response.json()
        # Need to push this into the geo or parsing segment of utils later
        if to_geojson:
            coordinates = [
                [
                    [float(point["longitude"]), float(point["latitude"])]
                    for point in boundary_data
                ]
            ]
            geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"name": neighbourhood_id},
                        "geometry": {"type": "Polygon", "coordinates": coordinates},
                    }
                ],
            }
            return geojson
        else:
            poly = ":".join(
                [f"{point['latitude']},{point['longitude']}" for point in boundary_data]
            )
            return poly

    async def get_people(self, force_id: str) -> List[Person]:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.

        Returns:
            A list of people (officers) in a specific police force.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}/people"
        )
        people_data = response.json()
        return [Person(**person) for person in people_data]
