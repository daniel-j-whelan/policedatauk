"""Test fixtures."""

from typing import Generator

import pytest
import respx
from aiolimiter import AsyncLimiter
from respx import Mock

from policedatauk import PoliceClient


@pytest.fixture
def api_client() -> Generator[PoliceClient]:
    """Fixture to provide a PoliceClient instance."""
    client = PoliceClient()
    client.limiter = AsyncLimiter(1, 1.0)  # Set a low rate limit for testing
    yield client


@pytest.fixture
def police_mock_respx(api_client: PoliceClient) -> Generator[Mock]:
    """Fixture to provide a respx mock for the Police Data API."""
    with respx.mock(base_url=api_client.police_url) as mock:
        yield mock


def postcode_mock_respx(api_client: PoliceClient) -> Generator[Mock]:
    """Fixture to provide a respx mock for the Postcodes.io API."""
    with respx.mock(base_url=api_client.postcode_url) as mock:
        yield mock
