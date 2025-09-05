"""Utilities for geo parsing and data manipulation."""

import json
import re
from typing import Tuple

import pyproj
from shapely import wkt
from shapely.geometry import Point, Polygon, mapping
from shapely.ops import transform

from .validation import validate_lat, validate_lon

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

API_POLYGON_REGEX = re.compile(
    r"""
        ^(\d+\.\d+,\d+\.\d+(?:\:|$))+$
    """,
    re.VERBOSE,
)


def buffer_point(
    lat: float, lon: float, radius_m: float, output: str = "wkt"
) -> str:
    """
    Buffer a WGS84 point by a radius in metres and return WKT polygon.

    Parameters:
        lat: Latitude in degrees.
        lon: Longitude in degrees.
        radius_m: Buffer radius in metres.
        output: "wkt" (default) or "geojson"

    Returns:
        str: WKT representation of the buffered polygon.
    """
    validate_lat(lat)
    validate_lon(lon)
    wgs84 = pyproj.CRS("EPSG:4326")
    # Use Azimuthal Equidistant projection centered on the point for accuracy
    local_aeqd = pyproj.CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +units=m +datum=WGS84"
    )
    # ^ This one is for you Andy!

    # Transformers
    project_to_local = pyproj.Transformer.from_crs(
        wgs84, local_aeqd, always_xy=True
    ).transform
    project_to_wgs84 = pyproj.Transformer.from_crs(
        local_aeqd, wgs84, always_xy=True
    ).transform

    # Create point and buffer in metres
    point = Point(lon, lat)
    point_local = transform(project_to_local, point)
    buffered_local = point_local.buffer(radius_m, quad_segs=3)

    # Reproject back to WGS84
    buffered_wgs84 = transform(project_to_wgs84, buffered_local)

    if output.lower() == "geojson":
        return json.dumps(mapping(buffered_wgs84))
    else:
        return buffered_wgs84.wkt


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
        match = API_POLYGON_REGEX.match(polygon.strip())
        if match:
            return polygon
        polygon_obj = wkt.loads(polygon)
        if not polygon_obj.is_valid:
            raise ValueError("Invalid polygon provided.")
        api_polygon = ":".join(
            f"{lat},{lon}" for lon, lat in polygon_obj.exterior.coords[:-1]
        )

    return api_polygon
