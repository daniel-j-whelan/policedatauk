import httpx
import asyncio
from aiolimiter import AsyncLimiter
from models import CrimeCategory, Force, ForceSummary, Person, PostCode
from typing import List
from utils import async_retry


class PoliceAPI:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.limiter = AsyncLimiter(max_rate=15, time_period=1.0)
        self.base_url = "https://data.police.uk/api"

    


    
    
    
    
    
    
    ### New changes ###
    
from models.location import CrimeReport

async def get_crimes_at_location(self, lat: float, lng: float, date: str | None = None) -> List[CrimeReport]:
    """Get crimes at a specific lat/lng. Optionally filter by date (YYYY-MM)."""
    url = f"https://data.police.uk/api/crimes-at-location?lat={lat}&lng={lng}"
    if date:
        url += f"&date={date}"
    response = await self._throttle_get_request(url)
    crimes_data = response.json()
    return [CrimeReport(**crime) for crime in crimes_data]
