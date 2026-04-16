"""Forces module for the policedatauk package."""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List, Literal, overload

import polars as pl

from ...models import Force, ForceSummary, Person
from ..resources import BaseResource
from ..transports import AsyncTransport, Transport


class AsyncForces(BaseResource):
    """Force-related Asynchronous API methods for the UK Police API.

    Args:
        transport: The Transport Client
    """

    def __init__(self, transport: AsyncTransport) -> None:
        """Initialise the AsyncForces class."""
        self.transport = transport

    @overload
    async def get_all_forces(
        self, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_all_forces(
        self, to_polars: Literal[False] = False
    ) -> List[ForceSummary]: ...

    async def get_all_forces(
        self, to_polars: bool = False
    ) -> pl.DataFrame | List[ForceSummary]:
        """Return a list of all police forces (basic summary only).

        Args:
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            All police forces (basic summary only).
        """
        response = await self.transport.request("GET", "/forces")
        forces = self._to_model_list(response.json(), ForceSummary)
        return self._format(forces, to_polars)

    @overload
    async def get_specific_force(
        self, force_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_specific_force(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> Force: ...

    async def get_specific_force(
        self, force_id: str, to_polars: bool = False
    ) -> pl.DataFrame | Force:
        """Return a specific police force by ID.

        Args:
            force_id: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific police force.
        """

        response = await self.transport.request("GET", f"/forces/{force_id}")
        model = self._to_model(response.json(), Force)
        return self._format(model, to_polars)

    @overload
    async def get_specific_forces(
        self, force_ids: List[str], to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_specific_forces(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> List[Force]: ...

    async def get_specific_forces(
        self, force_ids: List[str], to_polars: bool = False
    ) -> pl.DataFrame | List[Force]:
        """Return a list of police forces by ID in bulk.

        Args:
            force_ids: A list of police force IDs.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            Specific police forces.
        """
        tasks = [self.get_specific_force(force_id) for force_id in force_ids]
        forces = await asyncio.gather(*tasks, return_exceptions=True)
        valid_forces = [force for force in forces if isinstance(force, Force)]
        return self._format(valid_forces, to_polars)

    @overload
    async def get_people(
        self, force_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_people(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> List[Person]: ...

    async def get_people(
        self, force_id: str, to_polars: bool = False
    ) -> pl.DataFrame | List[Person]:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            People (officers) in a specific police force.
        """
        response = await self.transport.request(
            "GET", f"/forces/{force_id}/people"
        )
        models = self._to_model_list(response.json(), Person)
        return self._format(models, to_polars)


class Forces(BaseResource):
    """Force-related Synchronous API methods for the UK Police API.

    Args:
        transport (Transport): The Transport Client
    """

    def __init__(self, transport: Transport, max_workers: int = 10) -> None:
        """Initialise the Forces class."""
        self.transport = transport
        self.max_workers = max_workers

    @overload
    def get_all_forces(self, to_polars: Literal[True]) -> pl.DataFrame: ...

    @overload
    def get_all_forces(
        self, to_polars: Literal[False] = False
    ) -> List[ForceSummary]: ...

    def get_all_forces(
        self, to_polars: bool = False
    ) -> pl.DataFrame | List[ForceSummary]:
        """Return a list of all police forces (basic summary only).

        Args:
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            All police forces (basic summary only).
        """
        response = self.transport.request("GET", "/forces")
        forces = self._to_model_list(response.json(), ForceSummary)
        return self._format(forces, to_polars)

    @overload
    def get_specific_force(
        self, force_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_specific_force(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> Force: ...

    def get_specific_force(
        self, force_id: str, to_polars: bool = False
    ) -> pl.DataFrame | Force:
        """Return a specific police force by ID.

        Args:
            force_id: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            A specific police force.
        """

        response = self.transport.request("GET", f"/forces/{force_id}")
        model = self._to_model(response.json(), Force)
        return self._format(model, to_polars)

    @overload
    def get_specific_forces(
        self, force_ids: List[str], to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_specific_forces(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> List[Force]: ...

    def get_specific_forces(
        self, force_ids: List[str], to_polars: bool = False
    ) -> pl.DataFrame | List[Force]:
        """Return a list of police forces by ID in bulk.

        Args:
            force_ids: A list of police force IDs.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            Specific police forces.
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self.get_specific_force, force_id, False
                ): force_id
                for force_id in force_ids
            }
            valid_forces = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if isinstance(result, Force):
                        valid_forces.append(result)
                except Exception as e:
                    # Eventually log failure for specific IDs
                    pass

        return self._format(valid_forces, to_polars)

    @overload
    def get_people(
        self, force_id: str, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_people(
        self, force_id: str, to_polars: Literal[False] = False
    ) -> List[Person]: ...

    def get_people(
        self, force_id: str, to_polars: bool = False
    ) -> pl.DataFrame | List[Person]:
        """Return a list of people (officers) in a specific police force.

        Args:
            force_id: The ID of the police force.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            People (officers) in a specific police force.
        """
        response = self.transport.request("GET", f"/forces/{force_id}/people")
        models = self._to_model_list(response.json(), Person)
        return self._format(models, to_polars)
