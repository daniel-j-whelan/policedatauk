from pydantic import BaseModel, Field
from .location import StreetLocation
from typing import Dict, List, Optional


class CrimeCategory(BaseModel):
    """Represents a crime category.

    Args:
        name (str): Name of the crime category.
        url (str): URL of the crime category.
    """

    name: str = Field(..., description="Name of the crime category.")
    url: str = Field(..., description="URL of the crime category.")


class CrimeStatus(BaseModel):
    """Represents a crime status.

    Args:
        category (str): Category of the crime status.
        date (str): Date of the crime status.
    """

    category: str
    date: str


class CrimeReport(BaseModel):
    """Represents a crime report.

    Args:
        category (str): Category of the crime report.

        location_type (str): Location type of the crime report.

        location (StreetLocation): Location of the crime report.

        context (str): Context of the crime report.

        id (int): ID of the crime report.

        month (str): Month of the crime report.

        outcome_status (CrimeStatus | None, optional): Outcome status of the crime report.

        persistent_id (str | None, optional): Persistent ID of the crime report.
    """

    category: str
    location_type: Optional[str] = None
    location: Optional[StreetLocation] = None
    context: str
    id: int
    month: str
    outcome_status: CrimeStatus | None = None
    persistent_id: str | None = None


class LocationOutcome(BaseModel):
    """Represents a crime outcome.

    Args:
        category (Dict[str, str]): Category of the crime outcome.

        date (str): Date of the crime outcome.

        person_id (str | None, optional): Person ID of the crime outcome.

        crime (StreetLocation): Crime location of the crime outcome.
    """

    category: Dict[str, str]
    date: str
    person_id: str | None = None
    crime: StreetLocation


class CrimeOutcome(BaseModel):
    """Represents a crime outcome.

    Args:
        category (Dict[str, str]): Category of the crime outcome.

        date (str): Date of the crime outcome.

        person_id (str | None, optional): Person ID of the crime outcome.

        crime (StreetLocation): Crime location of the crime outcome.
    """

    category: Dict[str, str]
    date: str
    person_id: str | None = None


class CrimeWithOutcomes(BaseModel):
    crime: CrimeReport
    outcomes: List[CrimeOutcome]
