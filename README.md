# policedatauk

> A modern, async-first Python client for the [UK Police Data API](https://data.police.uk/), with Pydantic models and Polars integration.
> NOTE: This repository is still in development and the primary purpose is to understand good python packaging practices.

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: GPL](https://img.shields.io/badge/License-GPL-orange.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

---

## ✨ Features

* **Async-first**: Built on `httpx.AsyncClient` for fast, non-blocking API calls.
* **Typed models**: Pydantic v2 models wrap all responses for safe, validated data.
* **DataFrames out-of-the-box**: Convert results to [Polars](https://pola.rs) DataFrames for analysis and visualisation.
* **Rate limit handling**: Automatic throttling with retries and backoff.
* **Coverage**: Supports all major Police API endpoints, including:

  * Crimes
  * Outcomes
  * Forces & neighbourhoods
  * Stop & search
  * Postcode lookup

---

## 📦 Installation

```bash
pip install git+https://github.com/daniel-j-whelan/policedatauk.git
```

---

## 🚀 Examples

All `policedatauk` calls are **asynchronous**.  
- If you are running code in a **script or terminal**, wrap examples in `asyncio.run(...)`.  
- If you are running inside a **Jupyter notebook**, call the methods with `await` instead (since a loop is already running).

### Get Police Forces

```python
import asyncio
from policedatauk import PoliceClient

client = PoliceClient()

async def main():
    # List all police forces
    forces = await client.forces.get_all_forces()
    print(forces[:5])
    # Force(id='avon-and-somerset', name='Avon and Somerset Constabulary')

asyncio.run(main())
```

### Crimes by Force

```python
async def main():
    # Crimes in Avon & Somerset (January 2024)
    crimes = await client.crimes.get_crimes_no_location(
        date="2024-01",
        force="avon-and-somerset",
    )
    print(crimes[:5])
    # [CrimeReport(id='...', category='violent-crime', ...), ...]

asyncio.run(main())
```

### Results as a Polars DataFrame (to_polars)

```python
async def main():
    no_location_crimes_df = await client.crimes.get_crimes_no_location(
        date="2024-01",
        force="cambridgeshire",
        to_polars=True,
    )
    print(no_location_crimes_df.head(3))

asyncio.run(main())
```

### Get a Specific Crime by ID

```python
async def main():
    crime_id_df = await client.crimes.get_crime_by_id(
        crime_id="51e9616788041dfeeacb3c11ec40b9296c32213736f0ad16104173568f0dd4ce",
        to_polars=True
    )
    print(crime_id_df)

asyncio.run(main())
```

### Postcode Functionality

- Find a Postcode in the vicinity of a lat, lon coordinate

```python
async def main():
    find_postcodes_df = await client.postcodes.get_postcode(
        lat=53.2286,
        lon=-0.5478,
        to_polars=True
    )
    print(find_postcodes_df)

asyncio.run(main())
```

- Find more details about your postcode

```python
async def main():
    my_postcode_df = await client.postcodes.get_postcode_info(
        postcode="LN6 7TS",
        to_polars=True
    )
    print(my_postcode_df)

asyncio.run(main())
```

### Locate your Neighbourhood

```python
async def main():
    # Locate neighbourhood by coordinates
    neighbourhood_df = await client.neighbourhoods.locate_neighbourhood(
        lat=53.2286,
        lon=-0.5478,
        to_polars=True
    )
    print(neighbourhood_df)

    # Get neighbourhood boundaries (GeoJSON + shapely Polygon)
    geojson, poly = await client.neighbourhoods.get_boundary(
        force="lincolnshire",
        neighbourhood_id="NC14",
    )
    print(poly)

asyncio.run(main())
```

### Crimes Within a Polygon (e.g. a Neighbourhood boundary)

```python
async def main():
    # Get neighbourhood boundary polygon
    _, poly = await client.neighbourhoods.get_boundary(
        force="lincolnshire",
        neighbourhood_id="NC14",
    )

    # Crimes inside polygon
    crimes_in_poly_df = await client.crimes.get_crimes_by_location(
        date="2024-01",
        poly=poly,
        to_polars=True
    )
    print(crimes_in_poly_df.head())

    # Example: filter and group
    shoplifting_df = (
        crimes_in_poly_df
        .filter(crimes_in_poly_df["crime_code"] == "shoplifting")
        .group_by("outcome_code")
        .len()
        .sort("len", descending=True)
    )
    print(shoplifting_df)

asyncio.run(main())
```

### Crime Categories

```python
async def main():
    categories_df = await client.crimes.get_crime_categories(to_polars=True)
    print(categories_df)

asyncio.run(main())
```

### Notes
- In Jupyter notebooks, drop the asyncio.run(main()) wrapper and just use await directly:

```python
forces = await client.forces.get_all_forces()
forces[:3]
```

- All DataFrame examples use Polars. If to_polars=True is passed, results are returned as pl.DataFrame objects, otherwise they are returned as Pydantic models.
---


## 🌍 Geo support

COMING SOON - map integration to display crimes and locations using folium

---

## 🧪 Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/daniel-j-whelan/policedatauk.git
cd policedatauk
pip install -e ".[dev]"
```

Run tests:

```bash
uv run pytest
```

Lint and type check:

```bash
uv run ruff format
uv run ruff check --fix

```

---

## 📜 License

This project is licensed under the GNU General Public License – see [LICENSE.md](LICENSE.md) for details.
