# How to test the policedatauk package

`policedatauk` uses `pytest`, `pytest-cov` and `pytest-asyncio` for testing.

It is recommended to use a virtual environment before running any tests. This
library uses `uv` to manage this and the following commands from the root of the
directory will run the tests.

```bash
pip install uv

uv run pytest --cov-report=term --cov=policedatauk
```