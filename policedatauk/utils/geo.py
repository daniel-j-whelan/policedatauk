import json

import pyproj
from shapely.geometry import Point, mapping
from shapely.ops import transform

from .validation import validate_lat, validate_lon


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
    # Use an Azimuthal Equidistant projection centered on the point for local accuracy
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
