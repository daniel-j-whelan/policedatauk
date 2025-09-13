"""Tests for forces-related functionality."""

import pytest
from respx import MockRouter

from policedatauk import AsyncClient


@pytest.mark.asyncio
async def test_get_all_forces(
    api_client: AsyncClient, police_mock_respx: MockRouter
) -> None:
    """Tests that the get_all_forces method returns the expected result.

    Args:
        api_client (AsyncClient): The AsyncClient instance.
        mock_respx (Mock): The respx mock.
    """
    mock_route = police_mock_respx.get("/forces").respond(
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
