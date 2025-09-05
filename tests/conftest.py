"""Test fixtures."""

from typing import Generator

import pytest
import respx
from aiolimiter import AsyncLimiter

from policedatauk import PoliceClient


@pytest.fixture
def api_client() -> Generator[PoliceClient, None, None]:
    """Fixture to provide a PoliceClient instance."""
    client = PoliceClient()
    client.limiter = AsyncLimiter(1, 1.0)  # Set a low rate limit for testing
    yield client

@pytest.fixture(autouse=True)
def fast_retries(monkeypatch):
    """Make tenacity retries run instantly during tests (no sleep/wait)."""

    async def instant_sleep(_delay, *args, **kwargs):
        return None

    # Patch asyncio.sleep everywhere
    monkeypatch.setattr("asyncio.sleep", instant_sleep)

@pytest.fixture
def police_mock_respx(
    api_client: PoliceClient,
) -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock for the Police Data API."""
    with respx.mock(base_url=api_client.police_url) as mock:
        yield mock


@pytest.fixture
def postcode_mock_respx(
    api_client: PoliceClient,
) -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock for the Postcodes.io API."""
    with respx.mock(base_url=api_client.postcode_url) as mock:
        yield mock
