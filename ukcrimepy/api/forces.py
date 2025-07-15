import asyncio
import polars as pl
from .base import BaseAPI
from models.force import Force, ForceSummary, Person
from typing import List


class ForceAPI(BaseAPI):
    async def get_all_forces(self, to_polars: bool = False) -> List[Force]:
        """Return a list of all police forces (basic summary only).

        Args:
            to_polars (bool, optional): If True, return a Polars DataFrame. Defaults to False.

        Returns:
            List[Force]: A list of all police forces (basic summary only).
        """
        response = await self._throttle_get_request(f"{self.base_url}/forces")
        forces_data = response.json()
        if to_polars:
            return pl.json_normalize(forces_data)
        return [ForceSummary(**force_data) for force_data in forces_data]

    async def get_force(self, force_id: str) -> Force:
        """Return a specific police force by ID.

        Args:
            force_id (str): The ID of the police force.

        Returns:
            Force: A specific police force.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}"
        )
        force_data = response.json()
        force = Force(**force_data)
        return force

    async def get_specific_forces(self, force_ids: List[str]) -> List[Force]:
        """Return a list of police forces by ID in bulk.

        Args:
            force_ids (List[str]): A list of police force IDs.

        Returns:
            List[Force]: A list of police forces.
        """
        tasks = [self.get_force(force_id) for force_id in force_ids]
        return await asyncio.gather(*tasks)

    async def get_people(self, force_id: str) -> List[Person]:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id (str): The ID of the police force.

        Returns:
            List[Person]: A list of people (officers) in a specific police force.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}/people"
        )
        people_data = response.json()
        return [Person(**person) for person in people_data]
