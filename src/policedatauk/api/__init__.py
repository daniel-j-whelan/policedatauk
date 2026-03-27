"""Initialisation file for the api submodule."""

from .client import AsyncClient, Client
from .resources.base import BaseResource
from .resources.crimes import AsyncCrimes, Crimes
from .resources.forces import AsyncForces, Forces
from .resources.neighbourhoods import AsyncNeighbourhoods, Neighbourhoods
from .resources.postcodes import AsyncPostcodes, Postcodes

__all__ = [
    "BaseResource",
    "AsyncCrimes",
    "Crimes",
    "AsyncForces",
    "Forces",
    "AsyncNeighbourhoods",
    "Neighbourhoods",
    "AsyncPostcodes",
    "Postcodes",
]
