"""Overarching API client for the policedatauk package."""

from functools import cached_property

import httpx
from aiolimiter import AsyncLimiter

from ..utils import Limiter
from .crimes import AsyncCrimeAPI, CrimeAPI
from .forces import AsyncForceAPI, ForceAPI
from .neighbourhoods import AsyncNeighbourhoodAPI, NeighbourhoodAPI
from .postcodes import AsyncPostcodeAPI, PostcodeAPI
from .transports import AsyncTransport, Transport


class AsyncClient:
    """Class for asyncronous interaction with UK Police & Postcodes.io API.

    Args:
        transport (AsyncTransport): The HTTP transport.
        police_url (str): The base URL for the Police API.
        postcode_url (str): The base URL for the Postcodes.io API.
        crimes (CrimeAPI): The Crimes API.
        forces (ForceAPI): The Forces API.
        neighbourhoods (NeighbourhoodAPI): The Neighbourhoods API.
        postcodes (PostcodeAPI): The Postcodes API.
    """

    def __init__(self) -> None:
        """Initialise the PoliceClient class."""
        transport = AsyncTransport(httpx.AsyncClient(), AsyncLimiter(15, 1.0))
        self.police_url = "https://data.police.uk/api"
        self.postcode_url = "https://api.postcodes.io/postcodes"
        self.crimes = AsyncCrimeAPI(transport, self.police_url)
        self.forces = AsyncForceAPI(transport, self.police_url)
        self.neighbourhoods = AsyncNeighbourhoodAPI(transport, self.police_url)
        self.postcodes = AsyncPostcodeAPI(transport, self.postcode_url)

    @cached_property
    async def last_updated(self) -> str:
        """Return the last updated date of the crimes database.

        Returns:
            The last updated date of the crimes database.
        """
        url = f"{self.police_url}/crime-last-updated"
        response = await self.post(url)
        return response.json()["date"]


class Client:
    """Class for synchronous interaction with UK Police & Postcodes.io API.

    Args:
        client (httpx.Client): The HTTP client.
        limiter (Limiter): The synchronous rate limiter.
        police_url (str): The base URL for the Police API.
        postcode_url (str): The base URL for the Postcodes.io API.
        crimes (CrimeAPI): The Crimes API.
        forces (ForceAPI): The Forces API.
        neighbourhoods (NeighbourhoodAPI): The Neighbourhoods API.
        postcodes (PostcodeAPI): The Postcodes API.
    """

    def __init__(self) -> None:
        """Initialise the PoliceClient class."""
        transport = Transport(httpx.Client(), Limiter(30, 15))
        self.police_url = "https://data.police.uk/api"
        self.postcode_url = "https://api.postcodes.io/postcodes"
        self.crimes = CrimeAPI(transport, self.police_url)
        self.forces = ForceAPI(transport, self.police_url)
        self.neighbourhoods = NeighbourhoodAPI(transport, self.police_url)
        self.postcodes = PostcodeAPI(transport, self.postcode_url)

    @cached_property
    def last_updated(self) -> str:
        """Return the last updated date of the crimes database.

        Returns:
            The last updated date of the crimes database.
        """
        url = f"{self.police_url}/crime-last-updated"
        response = self.post(url)
        return response.json()["date"]
