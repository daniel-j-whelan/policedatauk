from typing import Optional

from pydantic import BaseModel, Field


class NeighbourhoodLinks(BaseModel):
    """Represents a follow-on link for a neighbourhood.

    Neighbourhood links are used to enable the user to find more information about
    a neighbourhood, such as its website or social media profiles.

    Args:
        url (str): The URL of the follow-on link (e.g. a social media profile).

        description (str | None): An optional description of the follow-on link.

        title (str): The title of the follow-on link.

    Exceptions:
        ValidationError: If the data is invalid.
    """

    url: str = Field(
        ...,
        description="URL of the follow-on link.",
        examples=["http://www.leicester.gov.uk/"],
    )
    description: str | None = Field(
        None, description="Description of the follow-on link."
    )
    title: str = Field(
        ...,
        description="Title of the follow-on link.",
        examples=["Leicester City Council"],
    )


class NeighbourhoodResult(BaseModel):
    """Result from /locate-neighbourhood endpoint.

    Args:
        force (str): The ID of the police force.
        neighbourhood (str): The ID of the neighbourhood.
    """

    force: str
    neighbourhood: str


class NeighbourhoodSummary(BaseModel):
    """Represents the basic summary information returned by /neighbourhoods endpoint.

    Args:
        id (str): The ID of the neighbourhood.
        name (str): The name of the neighbourhood.

    Exceptions:
        ValidationError: If the data is invalid.
    """

    id: str = Field(
        ...,
        description="ID of the neighbourhood.",
        examples=["NC04"],
    )
    name: str = Field(
        ...,
        description="Name of the neighbourhood.",
        examples=["Cultural Quarter"],
    )


class NeighbourhoodLocation(BaseModel):
    """Represents a significant location within a neighbourhood.

    Args:
        name (str | None): Name of the location (if available).

        longitude (str): Longitude of the location.

        latitude (str): Latitude of the location.

        postcode (str | None): Postcode of the location.

        address (str | None): Address of the location.

        telephone (str | None): Telephone number of the location.

        type (str): Type of location, e.g. 'station' (police station).

        description (str | None): Description of the location.

    Exceptions:
        ValidationError: If the data is invalid.
    """

    name: str | None = Field(None, description="Name of the location.")
    longitude: str | None = Field(
        None, description="Longitude of the location."
    )
    latitude: str | None = Field(None, description="Latitude of the location.")
    postcode: str | None = Field(None, description="Postcode of the location.")
    address: str | None = Field(None, description="Address of the location.")
    telephone: str | None = Field(
        None, description="Telephone number of the location."
    )
    type: str = Field(..., description="Type of location, e.g. 'station'.")
    description: str | None = Field(
        None, description="Description of the location."
    )


class Neighbourhood(BaseModel):
    """Represents a neighbourhood.

    Neighbourhoods are areas within a police force's jurisdiction.

    Args:
        id (str): The ID of the neighbourhood.

        description (str): A description of the neighbourhood.

        contact_details (dict): Contact information for the neighbourhood.

        name (str): The name of the neighbourhood.

        links (list[NeighbourhoodLinks]): A list of follow-on links for the neighbourhood.

        centre (dict): The latitude and longitude of the neighbourhood's centre point.

        locations (list[dict]): A list of locations within the neighbourhood.

        url_force (str): The URL of the neighbourhood's website.

        population (str): The population of the neighbourhood.

    Exceptions:
        ValidationError: If the data is invalid.
    """

    contact_details: dict = Field(
        default_factory=dict,
        description="Contact information for the neighbourhood.",
    )
    name: str = Field(..., description="Name of the neighbourhood.")
    description: str | None = Field(
        None, description="Description of the neighbourhood."
    )
    links: list[NeighbourhoodLinks] = Field(
        ..., description="List of follow-on links."
    )
    id: str = Field(..., description="ID of the neighbourhood.")
    centre: dict = Field(
        ...,
        description="Latitude and longitude of the neighbourhood's centre point.",
    )
    locations: list[NeighbourhoodLocation] = Field(
        ..., description="List of locations within the neighbourhood."
    )
    url_force: str = Field(
        ..., description="URL of the neighbourhood's website."
    )
    population: str = Field(
        ..., description="Population of the neighbourhood."
    )


class Person(BaseModel):
    """Represents a person in a police force.

    Args:
        name (str): Full name of the officer.

        rank (str): Rank of the officer.

        bio (str): HTML-formatted biography text.

        contact_details (dict): Contact information if available.

    Exceptions:
        ValidationError: If the data is invalid.
    """

    name: str = Field(
        ..., description="Full name of the officer.", examples=["John Doe"]
    )
    rank: str = Field(
        ..., description="Rank of the officer.", examples=["Chief Constable"]
    )
    bio: Optional[str] = Field(
        None,
        description="HTML-formatted biography text.",
        examples=["<p>John Doe is the Chief Constable of...</p>"],
    )
    contact_details: dict = Field(
        default_factory=dict, description="Contact information if available."
    )
