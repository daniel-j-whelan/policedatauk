"""Overarching API client for the policedatauk package."""

from typing import Final

import httpx
from pyrate_limiter import (
    AbstractBucket,
    Duration,
    InMemoryBucket,
    Limiter,
    Rate,
)

from .resources.crimes import AsyncCrimes, Crimes
from .resources.forces import AsyncForces, Forces
from .resources.neighbourhoods import AsyncNeighbourhoods, Neighbourhoods
from .resources.postcodes import AsyncPostcodes, Postcodes
from .transports import AsyncTransport, Transport


class BaseClient:
    """Shared configuration for both clients."""

    def __init__(self) -> None:
        """The Base Client."""
        self.POLICE_URL: Final = "https://data.police.uk/api"
        self.POSTCODE_URL: Final = "https://api.postcodes.io/postcodes"
        self.DEFAULT_RATES = [
            Rate(30, Duration.SECOND),
            Rate(150, Duration.SECOND * 10),
        ]


class Client(BaseClient):
    """Main class for synchronous UK Police & Postcodes.io API interaction."""

    def __init__(self, bucket: AbstractBucket | None = None) -> None:
        """Initialise the PoliceClient class."""
        super().__init__()
        self.bucket = bucket or InMemoryBucket(self.DEFAULT_RATES)
        self.police_transport = Transport(
            base_url=self.POLICE_URL,
            client=httpx.Client(),
            limiter=Limiter(self.bucket),
        )
        self.postcode_transport = Transport(
            base_url=self.POSTCODE_URL,
            client=httpx.Client(),
            limiter=Limiter(self.bucket),
        )
        self.crimes = Crimes(self.police_transport)
        self.forces = Forces(self.police_transport)
        self.neighbourhoods = Neighbourhoods(self.police_transport)
        self.postcodes = Postcodes(self.postcode_transport)


class AsyncClient(BaseClient):
    """Main class for synchronous UK Police & Postcodes.io API interaction."""

    def __init__(self, bucket: AbstractBucket | None = None) -> None:
        """Initialise the PoliceClient class."""
        super().__init__()
        self.bucket = bucket or InMemoryBucket(self.DEFAULT_RATES)
        self.police_transport = AsyncTransport(
            base_url=self.POLICE_URL,
            client=httpx.AsyncClient(),
            limiter=Limiter(self.bucket),
        )
        self.postcode_transport = AsyncTransport(
            base_url=self.POSTCODE_URL,
            client=httpx.AsyncClient(),
            limiter=Limiter(self.bucket),
        )
        self.crimes = AsyncCrimes(self.police_transport)
        self.forces = AsyncForces(self.police_transport)
        self.neighbourhoods = AsyncNeighbourhoods(self.police_transport)
        self.postcodes = AsyncPostcodes(self.postcode_transport)
