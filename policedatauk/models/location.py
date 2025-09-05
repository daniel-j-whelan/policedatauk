from typing import Dict

from pydantic import BaseModel


class StreetLocation(BaseModel):
    """Represents a street location.

    Args:
        latitude (str): Latitude of the street location.

        longitude (str): Longitude of the street location.

        street (Dict[str, str]): Street details of the street location.
    """

    latitude: str
    longitude: str
    street: Dict[str, str | int]
