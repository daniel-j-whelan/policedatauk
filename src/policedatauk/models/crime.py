"""Crime-related pydantic models."""

from typing import List

from pydantic import BaseModel, Field

from .location import StreetLocation


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

        location_type (str | None): Location type of the crime report.
            Defaults to None.

        location (StreetLocation | None): Location of the crime report.
            Defaults to None.

        context (str): Context of the crime report.

        id (int): ID of the crime report.

        month (str): Month of the crime report.

        outcome_status (CrimeStatus | None): Outcome status of a crime report.
            Defaults to None.

        persistent_id (str | None): Persistent ID of the crime report.
            Defaults to None.
    """

    category: str
    location_type: str | None = None
    location: StreetLocation | None = None
    context: str
    id: int
    month: str
    outcome_status: CrimeStatus | None = None
    persistent_id: str | None = None


class OutcomeCategory(BaseModel):
    """Represents a crime outcome category.

    Args:
        code (str): Category code, e.g. 'under-investigation'
        name (str): Human name for the category

    """

    code: str = Field(
        ..., description="Category code, e.g. 'under-investigation'"
    )
    name: str = Field(..., description="Human name for the category")


class LocationOutcome(BaseModel):
    """Represents a crime outcome.

    Args:
        category (OutcomeCategory): Category of the crime outcome.

        date (str): Date of the crime outcome.

        person_id (str | None): Person ID of the crime outcome.

        crime (StreetLocation): Crime location of the crime outcome.
    """

    category: OutcomeCategory
    date: str
    person_id: str | None = None
    crime: StreetLocation


class CrimeOutcome(BaseModel):
    """Represents a crime outcome.

    Args:
        category (OutcomeCategory): Category of the crime outcome.
        date (str): Date of the crime outcome.
        person_id (str | None): Person ID of the crime outcome.
    """

    category: OutcomeCategory
    date: str
    person_id: str | None = None


class CrimeWithOutcomes(BaseModel):
    """Represents a crime report with its associated outcomes.

    Args:
        crime (CrimeReport): Crime report.
        outcomes (List[CrimeOutcome]): List of crime outcomes.

    """

    crime: CrimeReport
    outcomes: List[CrimeOutcome]
