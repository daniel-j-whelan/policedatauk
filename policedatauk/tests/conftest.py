import pytest
import respx
from aiolimiter import AsyncLimiter
from policedatauk import PoliceClient


@pytest.fixture
def api_client():
    """Fixture to provide a PoliceClient instance."""
    client = PoliceClient()
    client.limiter = AsyncLimiter(1, 1.0)  # Set a low rate limit for testing
    yield client


@pytest.fixture
def mock_respx(api_client):
    """Fixture to provide a respx mock for the Police Data API."""
    with respx.mock(base_url=api_client.police_url) as mock:
        yield mock
