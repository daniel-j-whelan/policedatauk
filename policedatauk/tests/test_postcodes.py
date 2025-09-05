"""Tests for postcode-related functionality."""

import pytest
from respx import Mock

from policedatauk import PoliceClient


@pytest.mark.asyncio
async def test_get_postcode(
    api_client: PoliceClient, postcode_mock_respx: Mock
) -> None:
    """Test that the get_postcode method returns the expected result.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.

    Raises:
        ValueError: If the postcode is not found.
    """
    mock_route = postcode_mock_respx.get("/forces").respond(
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

    postcode = await api_client.postcodes.get_postcode("BR8 7RE")

    assert len(postcode) == 2
    assert postcode.results.id == "Kent"
    assert postcode.results.country == "England"
    assert mock_route.called


@pytest.mark.asyncio
async def test_get_postcode_info(
    api_client: PoliceClient, postcode_mock_respx: Mock
) -> None:
    """Tests that the get_postcode_info method returns the expected result.

    Args:
        api_client (PoliceClient): The PoliceClient instance.
        mock_respx (Mock): The respx mock.

    Raises:
        ValueError: If the postcode is not found.
    """
    mock_route = postcode_mock_respx.get("/forces").respond(
        200,
        json=[
            {
                "id": "avon-and-somerset",
                "name": "Avon and Somerset Constabulary",
            },
            {"id": "bedfordshire", "name": "Bedfordshire Police"},
        ],
    )

    forces = await api_client.forces.get_all_forces()

    assert len(forces) == 2
    assert forces[0].admin_county == "avon-and-somerset"
    assert forces[1].name == "Bedfordshire Police"
    assert mock_route.called
