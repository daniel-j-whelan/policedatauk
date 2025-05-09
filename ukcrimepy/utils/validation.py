
def validate_lat(lat: float) -> None:
    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    
def validate_lon(lon: float) -> None:
    if lon < -180 or lon > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")