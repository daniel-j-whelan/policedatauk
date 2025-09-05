# policedatauk

> A modern, async-first Python client for the [UK Police Data API](https://data.police.uk/), with Pydantic models and Polars integration.

[![CI](https://github.com/daniel-j-whelan/policedatauk/actions/workflows/ci.yml/badge.svg)](https://github.com/daniel-j-whelan/policedatauk/actions)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
<!-- [![PyPI version](https://badge.fury.io/py/policedatauk.svg)](https://pypi.org/project/policedatauk/) -->
[![License: GPL](https://img.shields.io/badge/License-GPL-orange.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

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
        # Get all forcess
        forces = await client.forces.get_all_forces()
        print(forces[0])

        # Crimes in a polygon (January 2024)
        crimes = await client.crimes.get_crimes_no_location(
            date="2024-01",
            force=forces[0].id,
        )
        print(crimes)

asyncio.run(main())
```

---

## 📊 DataFrame integration

All Pydantic models can be normalised into Polars for analysis:

```python
from policedatauk.utils import pydantic_to_df


crimes_df = pydantic_to_df(crimes, rename_key="crime_reports")
crimes_df.filter(
    crimes_df["category"] == "violent-crime"
).groupby("street_name").count()
```

---

## 🌍 Geo support

COMING SOON - map integration to display crimes and locations

---

## 🧪 Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/daniel-j-whelan/policedatauk.git
cd policedatauk
pip install -e ".[dev,geo]"
```

Run tests:

```bash
uv run pytest policedatauk\tests
```

Lint and type check:

```bash
uv run ruff format
uv run ruff check --fix

```

---

## 📈 Roadmap

* [ ] Complete coverage of all Police API endpoints
* [ ] Synchronous wrapper (for non-async users)
* [ ] Map integration for location & crime visualisation
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

This project is licensed under the GNU General Public License – see [LICENSE.md](LICENSE.md) for details.