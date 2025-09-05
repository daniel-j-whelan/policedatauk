"""Tests for utility functions."""

import httpx
import pytest
from respx import MockRouter
from shapely.errors import GEOSException

from policedatauk import PoliceClient
from policedatauk.utils import (
    buffer_point,
    parse_polygon,
    validate_lat,
    validate_lon,
)


def test_validate_coordinates() -> None:
    """Tests that the coordinates are validated correctly.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.

    Raises:
        TypeError: If the latitude or longitude is not a number.
        ValueError: If the latitude or longitude is out of range.

    """
    validate_lat(51.5074)
    validate_lon(-0.1278)

    with pytest.raises(TypeError):
        validate_lat("one hundred")

    with pytest.raises(TypeError):
        validate_lon(None)

    with pytest.raises(ValueError):
        validate_lat(100.0)

    with pytest.raises(ValueError):
        validate_lon(-200.0)


def test_create_polygon() -> None:
    """Tests that the polygon is created correctly.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.

    Raises:
        GEOSException: If the polygon is not valid.

    """
    polygon = buffer_point(51.5074, -0.1278, 1000)
    assert polygon is not None
    assert polygon.startswith("POLYGON ((")

    fake_polygon = "A fake polygon"
    with pytest.raises(GEOSException):
        parse_polygon(fake_polygon)

    parsed_polygon = parse_polygon(polygon)
    assert isinstance(parsed_polygon, str)
    assert not parsed_polygon.startswith("POLYGON ((")


@pytest.mark.asyncio
async def test_rate_limit(
    api_client: PoliceClient, police_mock_respx: MockRouter
) -> None:
    """Test that the rate limit is handled correctly.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        police_mock_respx (Mock): The respx mock.

    Raises:
        HTTPStatusError: If the rate limit is exceeded.
    """
    mock_route = police_mock_respx.post("/crimes-no-location").respond(
        429, text="Rate limit exceeded"
    )

    with pytest.raises(httpx.HTTPStatusError):
        response = await api_client.crimes.get_crimes_no_location(
            date="2024-01", force="metropolitan"
        )
        assert response.status_code == 429
        assert response.text == "Rate limit exceeded"
    assert mock_route.called
