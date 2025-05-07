from pydantic import BaseModel, Field
from .location import StreetLocation
from typing import Dict

class CrimeCategory(BaseModel):
    name: str = Field(..., description="Name of the crime category.")
    url: str = Field(..., description="URL of the crime category.")

class CrimeStatus(BaseModel):
    category: str
    date: str

class CrimeReport(BaseModel):
    category: str
    location_type: str
    location: StreetLocation
    context: str
    id: int
    month: str
    outcome_status: CrimeStatus | None = None
    persistent_id: str | None = None

class CrimeOutcome(BaseModel):
    category: Dict[str, str]
    date: str
    person_id: str | None = None
    crime: StreetLocation