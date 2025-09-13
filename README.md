# policedatauk

> A modern, async-first Python client for the [UK Police Data API](https://data.police.uk/), with Pydantic models and Polars integration.
>
> NOTE: This repository is still in development and the primary purpose is to understand good python packaging practices.

---

## ✨ Features

* **Async-first (now with sync support)**: Built on `httpx.AsyncClient` for fast, non-blocking API calls, but also exposes a blocking `httpx.Client` for synchronous use-cases.
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

`policedatauk` supports **both asynchronous** and **synchronous** clients. Use `AsyncClient` for `async/await` usage and `Client` for blocking (synchronous) code.

* If you are running code in a **script or terminal** and want async behaviour, wrap examples in `asyncio.run(...)` when using `AsyncClient`.
* If you prefer **blocking** code, instantiate `Client` and call methods directly (no `await`, no `asyncio`).
* In a **Jupyter notebook**, use `await` with `AsyncClient` (no `asyncio.run`), or use `Client` synchronously.

### Async
#### Get Police Forces

```python
import asyncio
from policedatauk import AsyncClient

client = AsyncClient()

async def main():
    # List all police forces
    forces = await client.forces.get_all_forces()
    print(forces[:5])
    # Force(id='avon-and-somerset', name='Avon and Somerset Constabulary')

asyncio.run(main())
```

#### Crimes by Force

```python
async def main():
    crimes = await client.crimes.get_crimes_no_location(
        date="2024-01",
        force="avon-and-somerset",
    )
    print(crimes[:5])

asyncio.run(main())
```

#### Results as a Polars DataFrame (to_polars)

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

#### Get a Specific Crime by ID

```python
async def main():
    crime_id_df = await client.crimes.get_crime_by_id(
        crime_id="51e9616788041dfeeacb3c11ec40b9296c32213736f0ad16104173568f0dd4ce",
        to_polars=True
    )
    print(crime_id_df)

asyncio.run(main())
```

#### Postcode Functionality

* Find Postcodes near coordinates

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

* Find more details about your postcode (async)

```python
async def main():
    my_postcode_df = await client.postcodes.get_postcode_info(
        postcode="LN6 7TS",
        to_polars=True
    )
    print(my_postcode_df)

asyncio.run(main())
```

#### Locate your Neighbourhood

```python
async def main():
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

#### Crimes Within a Polygon (e.g. a Neighbourhood boundary)

```python
async def main():
    _, poly = await client.neighbourhoods.get_boundary(
        force="lincolnshire",
        neighbourhood_id="NC14",
    )

    crimes_in_poly_df = await client.crimes.get_crimes_by_location(
        date="2024-01",
        poly=poly,
        to_polars=True
    )
    print(crimes_in_poly_df.head())

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

#### Crime Categories

```python
async def main():
    categories_df = await client.crimes.get_crime_categories(to_polars=True)
    print(categories_df)

asyncio.run(main())
```

### Sync
#### Get Police Forces

```python
from policedatauk import Client

client = Client()

# List all police forces (blocking)
forces = client.forces.get_all_forces()
print(forces[:5])
```

#### Crimes by Force

```python
# blocking / synchronous
crimes = client.crimes.get_crimes_no_location(
    date="2024-01",
    force="avon-and-somerset",
)
print(crimes[:5])
```

#### Results as a Polars DataFrame (to_polars)

```python
no_location_crimes_df = client.crimes.get_crimes_no_location(
    date="2024-01",
    force="cambridgeshire",
    to_polars=True,
)
print(no_location_crimes_df.head(3))
```

#### Get a Specific Crime by ID

```python
crime_id_df = client.crimes.get_crime_by_id(
    crime_id="51e9616788041dfeeacb3c11ec40b9296c32213736f0ad16104173568f0dd4ce",
    to_polars=True,
)
print(crime_id_df)
```

#### Postcode Functionality

```python
find_postcodes_df = client.postcodes.get_postcode(
    lat=53.2286,
    lon=-0.5478,
    to_polars=True,
)
print(find_postcodes_df)
```

* Find more details about your postcode

```python
my_postcode_df = client.postcodes.get_postcode_info(
    postcode="LN6 7TS",
    to_polars=True,
)
print(my_postcode_df)
```

#### Locate your Neighbourhood

```python
neighbourhood_df = client.neighbourhoods.locate_neighbourhood(
    lat=53.2286,
    lon=-0.5478,
    to_polars=True,
)
print(neighbourhood_df)

# Get neighbourhood boundaries (GeoJSON + shapely Polygon)
geojson, poly = client.neighbourhoods.get_boundary(
    force="lincolnshire",
    neighbourhood_id="NC14",
)
print(poly)
```

#### Crimes Within a Polygon

```python
_, poly = client.neighbourhoods.get_boundary(
    force="lincolnshire",
    neighbourhood_id="NC14",
)

crimes_in_poly_df = client.crimes.get_crimes_by_location(
    date="2024-01",
    poly=poly,
    to_polars=True,
)
print(crimes_in_poly_df.head())
```

#### Crime Categories

```python
categories_df = client.crimes.get_crime_categories(to_polars=True)
print(categories_df)
```

---

### Notes

* In Jupyter notebooks, use `await` with `AsyncClient` (no `asyncio.run`), or call `Client` methods directly for synchronous code.

* All DataFrame examples use Polars. If `to_polars=True` is passed, results are returned as `pl.DataFrame` objects, otherwise they are returned as Pydantic models.

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
