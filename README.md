# policedatauk

> A modern, async-first Python client for the [UK Police Data API](https://data.police.uk/), with Pydantic models and Polars integration.

[![CI](https://github.com/daniel-j-whelan/policedatauk/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/ukcrimepy/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/policedatauk.svg)](https://pypi.org/project/policedatauk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

* **Async-first**: Built on `httpx.AsyncClient` for fast, non-blocking API calls.
* **Typed models**: Pydantic v2 models wrap all responses for safe, validated data.
* **DataFrames out-of-the-box**: Convert results to [Polars](https://pola.rs) DataFrames for analysis and visualisation.
* **Geo-ready**: Optional [Shapely](https://shapely.readthedocs.io/) + [PyProj](https://pyproj4.github.io/pyproj/stable/) support for polygons, WKT, and GeoJSON.
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
pip install policedatauk
```

With geo support (Shapely + PyProj):

```bash
pip install policedatauk[geo]
```

---

## 🚀 Quick start

```python
import asyncio
from policedatauk import PoliceClient

async def main():
    async with PoliceClient() as client:
        # Get all forces
        forces = await client.forces.get_all_forces()
        print(forces[0])

        # Crimes in a polygon (January 2024)
        crimes = await client.crimes.get_all_crimes(
            date="2024-01",
            poly="POLYGON (( ))"
        )
        print(crimes)

asyncio.run(main())
```

---

## 📊 DataFrame integration

All Pydantic models can be normalised into Polars for analysis:

```python
from ukcrimepy.utils import crime_reports_to_polars

df = crime_reports_to_polars(crimes)
df.filter(df["category"] == "violent-crime").groupby("street_name").count()
```

Support is included for:

* `CrimeReport` → flat table
* `CrimeWithOutcomes` → exploded table (crime × outcomes)
* More coming soon

---

## 🌍 Geo support

Optional extras enable polygon, WKT and GeoJSON utilities:

```python
from ukcrimepy.utils import boundary_to_geojson_and_wkt

geojson, wkt = boundary_to_geojson_and_wkt(boundary_data, "neighbourhood-id")
```

Install with:

```bash
pip install ukcrimepy[geo]
```

---

## 🧪 Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/yourusername/ukcrimepy.git
cd ukcrimepy
pip install -e ".[dev,geo]"
```

Run tests:

```bash
pytest
```

Lint and type check:

```bash
ruff check .
mypy .
```

---

## 📈 Roadmap

* [ ] Complete coverage of all Police API endpoints
* [ ] Synchronous wrapper (for non-async users)
* [ ] CLI tool for quick queries
* [ ] Docs site (MkDocs or Sphinx)
* [ ] More Polars utilities (e.g. pre-built visualisations)

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo & create a feature branch
* Write tests for new features or bugfixes
* Run `pytest` and `ruff check .` before PR
* Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 License

This project is licensed under the MIT License – see [LICENSE](LICENSE) for details.