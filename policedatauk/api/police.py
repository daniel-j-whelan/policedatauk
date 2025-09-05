"""Overarching API client for the policedatauk package."""

from functools import cached_property

import httpx
from aiolimiter import AsyncLimiter

from .crimes import CrimeAPI
from .forces import ForceAPI
from .neighbourhoods import NeighbourhoodAPI
from .postcodes import PostcodeAPI


class PoliceClient:
    """Main class for interacting with UK Police & Postcodes.io API."""

    def __init__(self) -> None:
        """Initialise the PoliceClient class."""
        self.client = httpx.AsyncClient()
        self.limiter = AsyncLimiter(15, 1.0)
        self.police_url = "https://data.police.uk/api"
        self.postcode_url = "https://api.postcodes.io/postcodes"
        self.crimes = CrimeAPI(self.client, self.limiter, self.police_url)
        self.forces = ForceAPI(self.client, self.limiter, self.police_url)
        self.neighbourhoods = NeighbourhoodAPI(
            self.client, self.limiter, self.police_url
        )
        self.postcodes = PostcodeAPI(
            self.client, self.limiter, self.postcode_url
        )

    @cached_property
    def last_updated(self) -> str:
        """Return the last updated date of the crimes database.

        Returns:
            The last updated date of the crimes database.
        """
        url = f"{self.police_url}/crime-last-updated"
        response = self._throttle_post_request(url)
        return response.json()["date"]
