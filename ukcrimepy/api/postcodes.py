from .base import BaseAPI
from models.postcode import PostCode


class PostcodeAPI(BaseAPI):
    async def get_postcode_info(self, postcode: str) -> dict:
        """Return the detailed information of a postcode.

        Args:
            postcode (str): The postcode to get information for.

        Returns:
            dict: The detailed information of the postcode.
        """
        postcode = postcode.replace(" ", "").upper()
        valid_postcode = await self.is_valid_postcode(postcode)
        if not valid_postcode:
            raise ValueError(f"Invalid postcode: {postcode}")
        
        response = await self._throttle_get_request(
            f"https://api.postcodes.io/postcodes/{postcode}"
        )
        data = response.json()
        if data["status"] != 200 or not data["result"]:
            raise ValueError(f"API error: {data.get('error', 'Unknown')}")
        return PostCode(**data["result"])

    async def get_postcode(self, lat: float, lon: float) -> PostCode:
        """Get the postcode for a specific lat/lon.

        Args:
            lat (float): The latitude.

            lon (float): The longitude.

        Returns:
            PostCode: The postcode.
        """
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
            postcode (str): The postcode to check.

        Returns:
            bool: True if the postcode is valid, False otherwise.
        """
        postcode = postcode.replace(" ", "").upper()
        response = await self._throttle_get_request(
            f"https://api.postcodes.io/postcodes/{postcode}/validate"
        )
        data = response.json()
        if data["status"] != 200:
            raise ValueError(f"API error: {data.get('error', 'Unknown')}")
        if data["result"] is None:
            return False
        return True
