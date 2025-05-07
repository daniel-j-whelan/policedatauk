from pydantic import BaseModel, Field
    
class EngagementMethod(BaseModel):
    """Represents a single engagement method for a police force.

    Engagement methods are used to describe the various ways in which a police force
    can be contacted or interacted with, such as social media, phone, or email.

    Args:
        url (str): The URL of the engagement method (e.g. a social media profile).

        type (str): The type of engagement method (e.g. facebook, twitter, etc.).

        description (str | None): An optional description of the engagement method.

        title (str): The title of the engagement method.

    Returns:
        None

    Exceptions:
        ValidationError: If the data is invalid.
    """

    url: str = Field(
        ...,
        description="URL of the engagement method.",
        examples=[
            "http://www.twitter.com/leicspolice",
            "http://www.facebook.com/leicspolice",
        ],
    )
    type: str | None = Field(
        None,
        description="Type of engagement method.",
        examples=["facebook", "twitter", "youtube"],
    )
    description: str | None = Field(
        None, description="Description of the engagement method."
    )
    title: str = Field(
        ...,
        description="Title of the engagement method.",
        examples=["facebook", "twitter", "youtube"],
    )


class ForceSummary(BaseModel):
    """Represents the basic summary information returned by /forces endpoint.

    Args:
        id (str): The ID of the police force.

        name (str): The name of the police force.

    Returns:
        None

    Exceptions:
        ValidationError: If the data is invalid.
    """

    id: str = Field(
        ...,
        description="ID of the police force.",
        examples=["leicestershire"],
    )
    name: str = Field(
        ...,
        description="Name of the police force.",
        examples=["Leicestershire Police"],
    )


class Force(BaseModel):
    """Represents a police force.

    Police forces are responsible for maintaining law and order in a given area.

    Args:
        description (str): A description of the police force.

        url (str): The URL of the police force's website.

        engagement_methods (list[EngagementMethod]): A list of engagement methods for the police force.

        telephone (str): The telephone number of the police force.

        id (str): The ID of the police force.

        name (str): The name of the police force.

    Returns:
        None

    Exceptions:
        ValidationError: If the data is invalid.
    """

    description: str | None = Field(
        None, description="Description of the police force."
    )
    url: str = Field(..., description="URL of the police force.")
    engagement_methods: list[EngagementMethod] = Field(
        ..., description="List of engagement methods."
    )
    telephone: str = Field(..., description="Telephone number of the police force.")
    id: str = Field(..., description="ID of the police force.")
    name: str = Field(..., description="Name of the police force.")


class Person(BaseModel):
    """Represents a person in a police force.

    Args:
        name (str): Full name of the officer.

        rank (str): Rank of the officer.

        bio (str): HTML-formatted biography text.

        contact_details (dict): Contact information if available.

    Returns:
        None

    Exceptions:
        ValidationError: If the data is invalid.
    """

    name: str = Field(
        ..., description="Full name of the officer.", examples=["John Doe"]
    )
    rank: str = Field(
        ..., description="Rank of the officer.", examples=["Chief Constable"]
    )
    bio: str = Field(
        ...,
        description="HTML-formatted biography text.",
        examples=["<p>John Doe is the Chief Constable of...</p>"],
    )
    contact_details: dict = Field(
        default_factory=dict, description="Contact information if available."
    )