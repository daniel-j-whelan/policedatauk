import asyncio
from .base import BaseAPI
from models.force import Force, ForceSummary, Person
from typing import List
from utils import async_retry


class ForceAPI(BaseAPI):
    async def get_all_forces(self) -> List[Force]:
        """Return a list of all police forces (basic summary only)."""
        response = await self._throttle_get_request(f"{self.base_url}/forces")
        forces_data = response.json()
        return [ForceSummary(**force_data) for force_data in forces_data]

    @async_retry()
    async def get_force(self, force_id: str) -> Force:
        """Return a specific police force by ID."""
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}"
        )
        force_data = response.json()
        force = Force(**force_data)
        return force

    async def get_specific_forces(self, force_ids: List[str]) -> List[Force]:
        """Return a list of police forces by ID in bulk."""
        tasks = [self.get_force(force_id) for force_id in force_ids]
        return await asyncio.gather(*tasks)

    async def get_people(self, force_id: str) -> List[Person]:
        """Return a list of people (officers) in a specific police force."""
        response = await self._throttle_get_request(
            f"{self.base_url}/forces/{force_id}/people"
        )
        people_data = response.json()
        return [Person(**person) for person in people_data]
