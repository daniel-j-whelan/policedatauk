"""Tests for crimes-related functionality."""

import polars as pl
import pytest
from respx import Mock

from policedatauk import PoliceClient
from policedatauk.utils.dataframe import pydantic_to_df


@pytest.mark.asyncio
async def test_crimes_no_location(
    api_client: PoliceClient, police_mock_respx: Mock
) -> None:
    """Tests get_crimes_no_location returns the expected result.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.
    """
    mock_route = police_mock_respx.post("/crimes-no-location").respond(
        200,
        json=[
            {
                "category": "bicycle-theft",
                "location_type": None,
                "location": None,
                "context": "",
                "outcome_status": {
                    "category": (
                        "Investigation complete; no suspect identified",
                    ),
                    "date": "2024-01",
                },
                "persistent_id": (
                    "5fff4afc6584ac56744081c3eb0be8d1fce093acee4d2d754e60944f1d5bd43d",
                ),
                "id": 116072527,
                "location_subtype": "",
                "month": "2024-01",
            },
            {
                "category": "burglary",
                "location_type": None,
                "location": None,
                "context": "",
                "outcome_status": {
                    "category": (
                        "Investigation complete; no suspect identified",
                    ),
                    "date": "2024-01",
                },
                "persistent_id": (
                    "1b793a5cb34177d9dc9cc693ec026d04d8fe0910f31f7c062f3ea17c7f3057c5",
                ),
                "id": 116072457,
                "location_subtype": "",
                "month": "2024-01",
            },
        ],
    )

    crimes = await api_client.crimes.get_crimes_no_location(
        date="2024-01", force="metropolitan"
    )

    assert len(crimes) == 2
    assert crimes[0].id == 116072527
    assert (
        crimes[1].persistent_id
        == "1b793a5cb34177d9dc9cc693ec026d04d8fe0910f31f7c062f3ea17c7f3057c5"
    )
    assert mock_route.called


async def test_crimes_by_location(
    api_client: PoliceClient, police_mock_respx: Mock
) -> None:
    """Tests get_crimes_by_location returns the expected result.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.
    """
    mock_route = police_mock_respx.post("/crimes-street/all-crime").respond(
        200,
        json=[
            {
                "category": "anti-social-behaviour",
                "location_type": "Force",
                "location": {
                    "latitude": "52.343315",
                    "street": {
                        "id": 2043533,
                        "name": "On or near Kennedy Road",
                    },
                    "longitude": "0.417594",
                },
                "context": "",
                "outcome_status": None,
                "persistent_id": "",
                "id": 115918022,
                "location_subtype": "",
                "month": "2024-01",
            },
            {
                "category": "anti-social-behaviour",
                "location_type": "Force",
                "location": {
                    "latitude": "52.342091",
                    "street": {
                        "id": 2043502,
                        "name": "On or near Supermarket",
                    },
                    "longitude": "0.409276",
                },
                "context": "",
                "outcome_status": None,
                "persistent_id": "",
                "id": 115918552,
                "location_subtype": "",
                "month": "2024-01",
            },
        ],
    )

    crimes = await api_client.crimes.get_crimes_by_location(
        poly="52.268,0.543:52.794,0.238:52.130,0.478",
        date="2024-01",
    )
    assert len(crimes) == 2
    assert crimes[0].id == 115918022
    assert crimes[1].category == "anti-social-behaviour"

    crimes_df = pydantic_to_df(crimes, "crime_reports")
    assert isinstance(crimes_df, pl.DataFrame)
    assert mock_route.called


async def test_no_geo_params(api_client: PoliceClient) -> None:
    """Tests get_crimes_by_location fails when no geo params provided."""
    with pytest.raises(ValueError):
        await api_client.crimes.get_crimes_by_location()
