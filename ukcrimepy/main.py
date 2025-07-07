# import asyncio
# import time
# from .api import PoliceAPI
# from .utils import enable_police_api_logging


# async def test_get_all_forces():
#     print("\n🔍 TEST 1: Get all forces (1 request)")
#     start = time.perf_counter()
#     api = PoliceAPI()
#     forces = await api.get_forces()
#     print(f"✅ Retrieved {len(forces)} forces.")
#     print(f"⏱️ Time taken: {time.perf_counter() - start:.2f} seconds")


# async def test_get_5_forces():
#     print("\n🔁 TEST 2: Get 5 forces concurrently (well under limit)")
#     start = time.perf_counter()
#     api = PoliceAPI()
#     force_ids = [
#         "leicestershire",
#         "avon-and-somerset",
#         "metropolitan",
#         "surrey",
#         "north-wales",
#     ]
#     forces = await api.get_forces_bulk(force_ids)
#     for force in forces:
#         print(f"✔️ {force.name}")
#     print(f"⏱️ Time taken: {time.perf_counter() - start:.2f} seconds")


# async def test_get_20_forces_with_rate_limiting():
#     print("\n🚦 TEST 3: Get 20 forces (to trigger rate limiting + retries)")
#     start = time.perf_counter()
#     api = PoliceAPI()
#     # Get all IDs first
#     all_forces = await api.get_forces()
#     force_ids = [force.id for force in all_forces[:20]]  # Limit to first 20
#     forces = await api.get_forces_bulk(force_ids)
#     print(f"✅ Retrieved {len(forces)} forces.")
#     print(f"⏱️ Time taken: {time.perf_counter() - start:.2f} seconds")


# async def test_get_postcode_info():
#     print("\n📍 TEST 4: Get postcode info")
#     start = time.perf_counter()
#     api = PoliceAPI()
#     postcode = "SW1A 1AA"  # Buckingham Palace
#     postcode_info = await api.get_postcode_info(postcode)
#     print(f"✅ Retrieved info for postcode {postcode}: {postcode_info}")
#     print(f"⏱️ Time taken: {time.perf_counter() - start:.2f} seconds")
#     print(f"Latitude: {postcode_info.latitude}, Longitude: {postcode_info.longitude}")

# async def test_get_crime_categories():
#     print("\n📊 TEST 5: Get crime categories")
#     start = time.perf_counter()
#     api = PoliceAPI()
#     categories = await api.get_crime_categories()
#     print(f"✅ Retrieved {len(categories)} crime categories.")
#     for category in categories:
#         print(f"✔️ {category.name} ({category.url})")
#     print(f"⏱️ Time taken: {time.perf_counter() - start:.2f} seconds")

# async def main():
#     # await test_get_all_forces()
#     # await test_get_5_forces()
#     # await test_get_20_forces_with_rate_limiting()

#     # await test_get_postcode_info()
#     await test_get_crime_categories()

# if __name__ == "__main__":
#     enable_police_api_logging()
#     asyncio.run(main())

import asyncio
import httpx
from aiolimiter import AsyncLimiter
from api.crimes import CrimeAPI
from api.forces import ForceAPI
from api.postcodes import PostcodeAPI


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

    crime_categories = await api.crimes.get_crime_categories()
    print(crime_categories)

    force_summaries = await api.forces.get_all_forces()
    for force in force_summaries:
        print(force.name)

    specific_forces = await api.forces.get_specific_forces(
        ["metropolitan", "leicestershire"]
    )
    for force in specific_forces:
        print(force)

    postcode_info = await api.postcodes.get_postcode_info("SW1A 1AA")
    print(postcode_info)

    crimes_at_location = await api.crimes.get_crimes_at_location(
        lat=51.5014, lon=-0.1419, date="2023-09"
    )
    for crime in crimes_at_location:
        print(f"{crime}")


if __name__ == "__main__":
    asyncio.run(main())
