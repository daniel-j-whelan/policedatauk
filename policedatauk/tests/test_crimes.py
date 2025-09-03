import pytest


@pytest.mark.asyncio
async def test_get_crimes_no_location(api_client, mock_respx):
    mock_route = mock_respx.post("/crimes-no-location").respond(
        200,
        json=[
            {
                "category": "bicycle-theft",
                "location_type": None,
                "location": None,
                "context": "",
                "outcome_status": {
                    "category": "Investigation complete; no suspect identified",
                    "date": "2024-01",
                },
                "persistent_id": "5fff4afc6584ac56744081c3eb0be8d1fce093acee4d2d754e60944f1d5bd43d",
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
                    "category": "Investigation complete; no suspect identified",
                    "date": "2024-01",
                },
                "persistent_id": "1b793a5cb34177d9dc9cc693ec026d04d8fe0910f31f7c062f3ea17c7f3057c5",
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
