from pydantic import BaseModel, Field
from typing import Dict

class StreetLocation(BaseModel):
    latitude: str
    longitude: str
    street: Dict[str, str]
