import re
from shapely.geometry import Polygon
from shapely import wkt
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


def parse_polygon(polygon: str | Polygon) -> str:
    """Parse a polygon string into the required format.

    Args:
        polygon: The polygon string to parse.

    Returns:
        str: The formatted polygon string ready for police data UK API use.

    Raises:
        ValueError if the polygon string is not valid.
    """
    if isinstance(polygon, Polygon):
        if not polygon.is_valid:
            raise ValueError("Invalid polygon provided.")
        api_polygon = ":".join(
            f"{lat},{lon}" for lon, lat in polygon.exterior.coords[:-1]
        )
    elif isinstance(polygon, str):
        polygon_obj = wkt.loads(polygon)
        if not polygon_obj.is_valid:
            raise ValueError("Invalid polygon provided.")
        api_polygon = ":".join(
            f"{lat},{lon}" for lon, lat in polygon_obj.exterior.coords[:-1]
        )

    return api_polygon
