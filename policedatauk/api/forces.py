import asyncio
from typing import List

from ..models import Force, ForceSummary, Person
from .base import BaseAPI


class ForceAPI(BaseAPI):
    """Force-related API methods for the UK Police API."""

    async def get_all_forces(self) -> List[Force]:
        """Return a list of all police forces (basic summary only).

        Returns:
            A list of all police forces (basic summary only).
        """
        response = await self._throttle_get_request(f"{self.base_url}/forces")
        forces_data = response.json()
        return [ForceSummary(**force) for force in forces_data]

    async def get_force(self, force_id: str) -> Force:
        """Return a specific police force by ID.

        Args:
            force_id: The ID of the police force.

        Returns:
            A specific police force.
        """
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}"
        )
        force_data = response.json()
        return Force(**force_data)

    async def get_specific_forces(self, force_ids: List[str]) -> List[Force]:
        """Return a list of police forces by ID in bulk.

        Args:
            force_ids: A list of police force IDs.

        Returns:
            A list of police forces.
        """
        tasks = [self.get_force(force_id) for force_id in force_ids]
        forces = await asyncio.gather(*tasks, return_exceptions=True)
        # Need to add logging here to explain when tasks fail?
        return [force for force in forces if not isinstance(force, Exception)]

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
