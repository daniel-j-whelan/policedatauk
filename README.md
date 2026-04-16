# policedatauk

> A modern, robust Python client for the [UK Police Data API](https://data.police.uk/), featuring built-in Pydantic v2 validation, native Polars integration, and first-class Sync & Async support.

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: GPL](https://img.shields.io/badge/License-GPL-orange.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

---

## ✨ Features

* **Dual Architecture:** Choose between a simple Synchronous client or a high-performance Asynchronous client (both `httpx` backed).
* **Type-Safe Models:** All API responses are rigorously validated and serialized using `pydantic` v2.
* **Native DataFrames:** Instantly convert deeply nested JSON API responses into clean, flat [Polars](https://pola.rs) DataFrames with a single argument (`to_polars=True`).
* **Resilience:** Built-in rate limiting, exponential backoff, and retry logic to gracefully handle API throttling.
* **Geospatial Support:** Reverse geocoding for postcodes, neighbourhood boundary polygon generation, and spatial crime filtering.

---

## 📦 Installation

Install via pip (or uv):

```bash
pip install git+https://github.com/daniel-j-whelan/policedatauk.git
```

---

## 🚀 Quick Start

The library provides two clients depending on your needs: `PoliceClient` for standard scripts and notebooks, and `AsyncPoliceClient` for high-concurrency web apps or data pipelines.

### Standard (Synchronous) Usage

```python
from policedatauk import PoliceClient

client = PoliceClient()

# List all police forces
forces = client.forces.get_all_forces()
print(forces[0].name) 
# Output: Avon and Somerset Constabulary

# Get crimes for a force as a Polars DataFrame
crimes_df = client.crimes.get_crimes_no_location(
    date="2024-01",
    force="avon-and-somerset",
    to_polars=True
)
print(crimes_df.head(3))
```

### High-Performance (Asynchronous) Usage

```python
import asyncio
from policedatauk import AsyncPoliceClient

async def main():
    client = AsyncPoliceClient()
    
    # Fetch crime categories
    categories = await client.crimes.get_crime_categories()
    print(categories[:3])

asyncio.run(main())
```
*(Note: If you are running code inside a Jupyter Notebook, an event loop is already running. You can drop `asyncio.run()` and use `await` directly.)*

---

## 💡 Advanced Examples

### Geospatial & Neighbourhoods
You can locate neighbourhoods via coordinates and extract their exact boundary polygons (returned as both GeoJSON and Shapely formats).

```python
from policedatauk import PoliceClient

client = PoliceClient()

# 1. Find neighbourhood by coordinates
neighbourhood = client.neighbourhoods.locate_neighbourhood(
    lat=53.2286,
    lon=-0.5478
)
print(f"Force: {neighbourhood.force}, Neighbourhood: {neighbourhood.neighbourhood}")

# 2. Get the boundary polygon
geojson, poly = client.neighbourhoods.get_boundary(
    force="lincolnshire",
    neighbourhood_id="NC14"
)

# 3. Find all crimes within that specific boundary
crimes_in_poly_df = client.crimes.get_crimes_by_location(
    date="2024-01",
    poly=poly,  # Automatically handles the POST request
    to_polars=True
)

# 4. Filter and Group using Polars
shoplifting_stats = (
    crimes_in_poly_df
    .filter(crimes_in_poly_df["crime_code"] == "shoplifting")
    .group_by("outcome_code")
    .len()
    .sort("len", descending=True)
)
print(shoplifting_stats)
```

### Postcode Resolution
The library seamlessly integrates with `postcodes.io` to translate real-world postcodes into usable coordinates for the Police API.

```python
from policedatauk import PoliceClient

client = PoliceClient()

# Get detailed info about a specific postcode
my_postcode = client.postcodes.get_postcode_info(postcode="LN6 7TS")
print(my_postcode.latitude, my_postcode.longitude)

# Find nearest postcodes to a coordinate
nearby_postcodes_df = client.postcodes.get_postcode(
    lat=53.2286,
    lon=-0.5478,
    to_polars=True
)
```

---

## 🛠️ Data Handling: Models vs. DataFrames

By default, all methods return highly structured **Pydantic Models**. This provides perfect IDE auto-completion and type safety.

If you are data-analysing, pass `to_polars=True`. The library will automatically:
1. Flatten deeply nested API responses.
2. Resolve empty strings and missing values.
3. Standardize column names across endpoints.
4. Return a highly optimized `pl.DataFrame`.

---

## 📜 License

This project is licensed under the GNU General Public License – see [LICENSE.md](LICENSE.md) for details.