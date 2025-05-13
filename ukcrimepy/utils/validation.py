
def validate_lat(lat: float) -> None:
    """
    Validate a latitude value.

    Args:
        lat (float): The latitude value to validate.

    Returns:
        True if the latitude is valid.

    Raises:
        ValueError if the latitude is not between -90 and 90 degrees.
    """
    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
        # return False
    return True

def validate_lon(lon: float) -> None:
    """Validate a longitude value.

    Args:
        lon (float): The longitude value to validate.

    Returns:
        True if the longitude is valid.

    Raises:
        ValueError if the longitude is not between -180 and 180 degrees.
    """
    if lon < -180 or lon > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")
        # return False
    return True