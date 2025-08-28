import re
from datetime import datetime


def validate_lat(lat: float) -> None:
    """Validate a latitude value.

    Args:
        lat: The latitude value to validate.

    Returns:
        True if the latitude is valid.

    Raises:
        TypeError if the latitude is not a float or string representation of a float.
        ValueError if the latitude is not between -90 and 90 degrees.
    """
    try:
        float(lat)
    except ValueError:
        raise TypeError("'lat' must be a float or a string representation of a float.")
    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
        # return False
    return True


def validate_lon(lon: float) -> None:
    """Validate a longitude value.

    Args:
        lon: The longitude value to validate.

    Returns:
        True if the longitude is valid.

    Raises:
        TypeError if the longitude is not a float or string representation of a float.
        ValueError if the longitude is not between -180 and 180 degrees.
    """
    try:
        float(lon)
    except ValueError:
        raise TypeError("'lon' must be a float or a string representation of a float.")
    if lon < -180 or lon > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")
        # return False
    return True


def validate_date(date: str) -> None:
    """Validate a date string in the format YYYY-MM.

    Args:
        date: The date string to validate.

    Returns:
        True if the date is valid.

    Raises:
        ValueError if the date is not in the correct format or is out of range.
    """

    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", date):
        raise ValueError("Date must be in the format YYYY-MM.")

    year, month = map(int, date.split("-"))
    current_year = datetime.now().year
    current_month = datetime.now().month

    if (
        year < 2022
        or (year == 2022 and month < 7)
        or (year == current_year and month > current_month)
        or year > current_year
    ):
        raise ValueError("Date must be between 2022-07 and the current month.")

    return True
