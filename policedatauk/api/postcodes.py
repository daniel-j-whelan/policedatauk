from httpx import HTTPStatusError

from ..models import PostCode
from ..utils import validate_lat, validate_lon
from .base import BaseAPI


class PostcodeAPI(BaseAPI):
    """Postcode-related API methods for the Postcodes.io API."""

    async def get_postcode_info(self, postcode: str) -> dict:
        """Return detailed information about a postcode.

        Args:
            postcode: The postcode to get information for.

        Returns:
            The detailed information of the postcode.
        """
        postcode = postcode.replace(" ", "").upper()
        valid_postcode = await self.is_valid_postcode(postcode)
        if not valid_postcode:
            # Need to create custom exception
            raise ValueError(f"Invalid postcode: {postcode}")
        try:
            response = await self._throttle_get_request(
                f"https://api.postcodes.io/postcodes/{postcode}"
            )
        # Need to handle HTTPStatusError separately to provide better error messages
        except HTTPStatusError as e:
            raise ValueError(f"API error: {e}")
        data = response.json()
        if data["status"] != 200 or not data["result"]:
            raise ValueError(f"API error: {data.get('error', 'Unknown')}")
        return PostCode(**data["result"])

    async def get_postcode(self, lat: float, lon: float) -> PostCode:
        """Get the postcode for a specific lat/lon.

        Args:
            lat: The latitude.

            lon: The longitude.

        Returns:
            PostCode: The postcode.
        """
        validate_lat(lat)
        validate_lon(lon)
        response = await self._throttle_get_request(
            f"https://api.postcodes.io/postcodes?lat={lat}&lon={lon}"
        )
        data = response.json()
        if data["status"] != 200 or not data["result"]:
            raise ValueError(f"API error: {data.get('error', 'Unknown')}")
        return PostCode(**data["result"])

    async def is_valid_postcode(self, postcode: str) -> bool:
        """Check if a postcode is valid.

        Args:
            postcode: The postcode to check.

        Returns:
            True if the postcode is valid, False otherwise.
        """
        postcode = postcode.replace(" ", "").upper()
        response = await self._throttle_get_request(
            f"https://api.postcodes.io/postcodes/{postcode}/validate"
        )
        data = response.json()
        if data["status"] != 200:
            raise ValueError(f"API error: {data.get('error', 'Unknown')}")
        # Result is either True or False
        return data["result"]
