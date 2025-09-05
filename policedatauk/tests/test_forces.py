import pytest


@pytest.mark.asyncio
async def test_get_all_forces(api_client, mock_respx):
    mock_route = mock_respx.get("/forces").respond(
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
    assert forces[0].id == "avon-and-somerset"
    assert forces[1].name == "Bedfordshire Police"
    assert mock_route.called
