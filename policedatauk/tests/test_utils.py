import pytest
import httpx
from policedatauk.utils import buffer_point, parse_polygon, validate_lat, validate_lon
from shapely.errors import GEOSException


def test_validate_coordinates():
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


def test_create_polygon():
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
async def test_rate_limit(api_client, mock_respx):
    mock_route = mock_respx.post("/crimes-no-location").respond(
        429, text="Rate limit exceeded"
    )

    with pytest.raises(httpx.HTTPStatusError):
        response = await api_client.crimes.get_crimes_no_location(
            date="2024-01", force="metropolitan"
        )
        assert response.status_code == 429
        assert response.text == "Rate limit exceeded"
    assert mock_route.called
