import re
from typing import Tuple

LAT_LON_REGEX = re.compile(
    r"""
        ^\s*                    # optional leading whitespace
        (-?\d+(?:\.\d+)?)       # latitude: group 1
        \s*[, ]\s*              # separator: comma, space, or both
        (-?\d+(?:\.\d+)?)       # longitude: group 2
        \s*$                    # optional trailing whitespace
    """,
    re.VERBOSE,
)


def parse_lat_lon(coord: str) -> Tuple[float, float]:
    """Parse a latitude/longitude pair from a flexible string format.

    Accepts formats like:
    - "52.123,-1.456"
    - "52.123, -1.456"
    - "52.123 -1.456"
    - "52.123    -1.456"
    - With or without trailing spaces

    Args:
        coord (str): The coordinate string to parse.

    Returns:
        Tuple[float, float]: The latitude and longitude.

    Raises:
        ValueError if the pattern doesn't match.
    """
    match = LAT_LON_REGEX.match(coord.strip())
    if not match:
        raise ValueError(f"Could not parse lat/lon from: {coord!r}")
    lat, lon = map(float, match.groups())
    return lat, lon
