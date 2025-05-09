import asyncio
import httpx
from aiolimiter import AsyncLimiter
from functools import cached_property
from crimes import CrimeAPI
from forces import ForceAPI
from postcodes import PostcodeAPI

class PoliceAPI:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.limiter = AsyncLimiter(15, 1.0)
        self.police_url = "https://data.police.uk/api"
        self.postcode_url = "https://api.postcodes.io/postcodes"
        self.crimes = CrimeAPI(self.client, self.limiter, self.police_url)
        self.forces = ForceAPI(self.client, self.limiter, self.police_url)
        self.postcodes = PostcodeAPI(self.client, self.limiter, self.postcode_url)


    @cached_property
    def last_updated(self) -> str:
        url = f"{self.police_url}/crime-last-updated"
        response = self.throttle_get_request(url)
        return response.json()["date"]

async def main():
    api = PoliceAPI()
    # Example usage
    crime_categories = await api.crimes.get_crime_categories()
    print(crime_categories)

    force_summaries = await api.forces.get_all_forces()
    for force in force_summaries:
        print(force.name)

if __name__ == "__main__":
    asyncio.run(main())
