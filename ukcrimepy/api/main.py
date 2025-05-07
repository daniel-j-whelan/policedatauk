import asyncio
import httpx
from aiolimiter import AsyncLimiter
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
        
        
async def main():
    api = PoliceAPI()
    # Example usage
    crime_categories = await api.crimes.get_crime_categories()
    print(crime_categories)
    
if __name__ == "__main__":
    asyncio.run(main())