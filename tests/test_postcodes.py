"""Tests for postcode-related functionality."""

import pytest
from respx import MockRouter

from policedatauk import AsyncClient


@pytest.mark.asyncio
async def test_get_postcode(
    api_client: AsyncClient, postcode_mock_respx: MockRouter
) -> None:
    """Test that the get_postcode method returns the expected result.

    Args:
        api_client (AsyncClient): The AsyncClient instance.
        postcode_mock_respx (Mock): The respx mock.

    Raises:
        ValueError: If the postcode is not found.
    """
    mock_route = postcode_mock_respx.get().respond(
        200,
        json={
            "status": 200,
            "result": [
                {
                    "postcode": "SW1A 2DD",
                    "quality": 1,
                    "eastings": 530075,
                    "northings": 180339,
                    "country": "England",
                    "nhs_ha": "London",
                    "longitude": -0.127149,
                    "latitude": 51.50702,
                    "european_electoral_region": "London",
                    "primary_care_trust": "Westminster",
                    "region": "London",
                    "lsoa": "Westminster 018C",
                    "msoa": "Westminster 018",
                    "incode": "2DD",
                    "outcode": "SW1A",
                    "parliamentary_constituency": (
                        "Cities of London and Westminster"
                    ),
                    "parliamentary_constituency_2024": (
                        "Cities of London and Westminster"
                    ),
                    "admin_district": "Westminster",
                    "parish": "Westminster, unparished area",
                    "admin_county": None,
                    "date_of_introduction": "198001",
                    "admin_ward": "St James's",
                    "ced": None,
                    "ccg": "NHS North West London",
                    "nuts": "Westminster",
                    "pfa": "Metropolitan Police",
                    "codes": {
                        "admin_district": "E09000033",
                        "admin_county": "E99999999",
                        "admin_ward": "E05013806",
                        "parish": "E43000236",
                        "parliamentary_constituency": "E14001172",
                        "parliamentary_constituency_2024": "E14001172",
                        "ccg": "E38000256",
                        "ccg_id": "W2U3Z",
                        "ced": "E99999999",
                        "nuts": "TLI35",
                        "lsoa": "E01004736",
                        "msoa": "E02000977",
                        "lau2": "E09000033",
                        "pfa": "E23000001",
                    },
                    "distance": 10.58165325,
                }
            ],
        },
    )

    postcode = await api_client.postcodes.get_postcode(lat=51.507, lon=-0.127)

    assert len(postcode) == 1
    assert postcode[0].nhs_ha == "London"
    assert postcode[0].ccg == "NHS North West London"
    assert mock_route.called


@pytest.mark.asyncio
async def test_get_postcode_info(
    api_client: AsyncClient, postcode_mock_respx: MockRouter
) -> None:
    """Tests that the get_postcode_info method returns the expected result.

    Args:
        api_client (AsyncClient): The AsyncClient instance.
        postcode_mock_respx (Mock): The respx mock.

    Raises:
        ValueError: If the postcode is not found.
    """
    mock_validate_route = postcode_mock_respx.get("/BR87RE/validate").respond(
        200,
        json={"status": 200, "result": True},
    )
    mock_info_route = postcode_mock_respx.get("/BR87RE").respond(
        200,
        json={
            "status": 200,
            "result": {
                "postcode": "BR8 7RE",
                "quality": 1,
                "eastings": 551626,
                "northings": 170342,
                "country": "England",
                "nhs_ha": "South East Coast",
                "longitude": 0.178897,
                "latitude": 51.411831,
                "european_electoral_region": "South East",
                "primary_care_trust": "West Kent",
                "region": "South East",
                "lsoa": "Sevenoaks 001A",
                "msoa": "Sevenoaks 001",
                "incode": "7RE",
                "outcode": "BR8",
                "parliamentary_constituency": "Sevenoaks",
                "parliamentary_constituency_2024": "Sevenoaks",
                "admin_district": "Sevenoaks",
                "parish": "Hextable",
                "admin_county": "Kent",
                "date_of_introduction": "198001",
                "admin_ward": "Hextable",
                "ced": "Swanley",
                "ccg": "NHS Kent and Medway",
                "nuts": "Sevenoaks",
                "pfa": "Kent",
                "codes": {
                    "admin_district": "E07000111",
                    "admin_county": "E10000016",
                    "admin_ward": "E05009960",
                    "parish": "E04012394",
                    "parliamentary_constituency": "E14001465",
                    "parliamentary_constituency_2024": "E14001465",
                    "ccg": "E38000237",
                    "ccg_id": "91Q",
                    "ced": "E58000739",
                    "nuts": "TLJ46",
                    "lsoa": "E01024445",
                    "msoa": "E02005087",
                    "lau2": "E07000111",
                    "pfa": "E23000032",
                },
            },
        },
    )

    postcode = await api_client.postcodes.get_postcode_info("BR8 7RE")

    assert postcode.admin_county == "Kent"
    assert postcode.country == "England"
    assert mock_validate_route.called
    assert mock_info_route.called
