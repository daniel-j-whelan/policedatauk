"""Utilities for working with dates."""

from datetime import date, timedelta


def get_last_month() -> str:
    """Gets the last month in the Police data API format, YYYY-MM

    Returns:
        The last month in the Police data API format
    """
    today = date.today().replace(day=1)
    last_month = today - timedelta(days=1)
    return last_month.strftime("%Y-%m")
