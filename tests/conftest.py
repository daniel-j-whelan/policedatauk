"""Test fixtures."""

from typing import Generator

import pytest
import respx
from aiolimiter import AsyncLimiter

from policedatauk import AsyncClient


@pytest.fixture
def api_client() -> Generator[AsyncClient, None, None]:
    """Fixture to provide an AsyncClient instance."""
    client = AsyncClient()
    client.limiter = AsyncLimiter(1, 1.0)  # Set a low rate limit for testing
    yield client


@pytest.fixture(autouse=True)
def fast_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make tenacity retries run instantly during tests (no sleep/wait)."""

    async def instant_sleep(_delay: float) -> None:
        return None

    # Patch asyncio.sleep everywhere when testing
    monkeypatch.setattr("asyncio.sleep", instant_sleep)


@pytest.fixture
def police_mock_respx(
    api_client: AsyncClient,
) -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock for the Police Data API."""
    with respx.mock(base_url=api_client.police_url) as mock:
        yield mock


@pytest.fixture
def postcode_mock_respx(
    api_client: AsyncClient,
) -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock for the Postcodes.io API."""
    with respx.mock(base_url=api_client.postcode_url) as mock:
        yield mock
