# ukcrimepy

A modern, async Python wrapper for the UK Police Data API.

## Features

- Get crime data and look at locations of interest
- check out local police forces
- Async-powered with httpx + asyncio
- Built-in rate limiting and retries
- Pydantic-validated models

## Usage

```python
from ukcrimepy import PoliceAPI

api = PoliceAPI()
