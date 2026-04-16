"""Postcode module for the policedatauk package."""

from typing import Any, List, Literal, overload

import polars as pl
from httpx import HTTPStatusError

from ...models import PostCode
from ...utils import pydantic_to_df, validate_lat, validate_lon
from ..resources import BaseResource
from ..transports import AsyncTransport, Transport


class AsyncPostcodes(BaseResource):
    """Postcode-related Asynchronous API methods for the Postcodes.io API.

    Args:
        transport: The Transport Client
    """

    def __init__(self, transport: AsyncTransport) -> None:
        """Initialise the AsyncPostcodes class."""
        self.transport = transport

    async def is_valid_postcode(self, postcode: str) -> bool:
        """Check if a postcode is valid.

        Args:
            postcode: The postcode to check.

        Returns:
            True if the postcode is valid, False otherwise.
        """
        postcode = postcode.replace(" ", "").upper()
        response = await self.transport.request("GET", f"/{postcode}/validate")
        data = response.json()
        return data.get("result", False)

    @overload
    async def get_postcode_info(
        self, postcode: str, *, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_postcode_info(
        self, postcode: str, *, to_polars: Literal[False] = False
    ) -> PostCode: ...

    async def get_postcode_info(
        self, postcode: str, to_polars: bool = False
    ) -> pl.DataFrame | PostCode:
        """Return detailed information about a postcode.

        Args:
            postcode: The postcode to get information for.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            The detailed information of the postcode.
        """
        postcode = postcode.replace(" ", "").upper()
        if not await self.is_valid_postcode(postcode):
            raise ValueError(f"Invalid postcode provided: '{postcode}'")

        try:
            response = await self.transport.request("GET", f"/{postcode}")
        except HTTPStatusError as e:
            raise ValueError(
                f"Postcodes.io API error: {e.response.text}"
            ) from e

        data = response.json().get("result")
        model = self._to_model(data, PostCode)
        return self._format(model, to_polars)

    @overload
    async def get_postcode(
        self, *, lat: float, lon: float, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    async def get_postcode(
        self, *, lat: float, lon: float, to_polars: Literal[False] = False
    ) -> List[PostCode]: ...

    async def get_postcode(
        self, *, lat: float, lon: float, to_polars: bool = False
    ) -> pl.DataFrame | List[PostCode]:
        """Get the postcode for a specific lat/lon.

        Args:
            lat: The latitude.
            lon: The longitude.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            PostCode: The postcode.
        """
        validate_lat(lat)
        validate_lon(lon)

        params = {"lat": lat, "lon": lon}

        try:
            response = await self.transport.request("GET", params=params)
        except HTTPStatusError as e:
            raise ValueError(
                f"Postcodes.io API error: {e.response.text}"
            ) from e

        # The API returns null or a list inside 'result'
        data = response.json().get("result") or []

        models = self._to_model_list(data, PostCode)
        return self._format(models, to_polars)


class Postcodes(BaseResource):
    """Postcode-related Synchronous API methods for the Postcodes.io API.

    Args:
        transport: The Transport Client
    """

    def __init__(self, transport: Transport) -> None:
        """Initialise the Postcodes class."""
        self.transport = transport

    def is_valid_postcode(self, postcode: str) -> bool:
        """Check if a postcode is valid.

        Args:
            postcode: The postcode to check.

        Returns:
            True if the postcode is valid, False otherwise.
        """
        postcode = postcode.replace(" ", "").upper()
        response = self.transport.request("GET", f"/{postcode}/validate")
        data = response.json()
        return data.get("result", False)

    @overload
    def get_postcode_info(
        self, postcode: str, *, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_postcode_info(
        self, postcode: str, *, to_polars: Literal[False] = False
    ) -> PostCode: ...

    def get_postcode_info(
        self, postcode: str, to_polars: bool = False
    ) -> pl.DataFrame | PostCode:
        """Return detailed information about a postcode.

        Args:
            postcode: The postcode to get information for.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            The detailed information of the postcode.
        """
        postcode = postcode.replace(" ", "").upper()
        if not self.is_valid_postcode(postcode):
            raise ValueError(f"Invalid postcode provided: '{postcode}'")

        try:
            response = self.transport.request("GET", f"/{postcode}")
        except HTTPStatusError as e:
            raise ValueError(
                f"Postcodes.io API error: {e.response.text}"
            ) from e

        data = response.json().get("result")
        model = self._to_model(data, PostCode)
        return self._format(model, to_polars)

    @overload
    def get_postcode(
        self, *, lat: float, lon: float, to_polars: Literal[True]
    ) -> pl.DataFrame: ...

    @overload
    def get_postcode(
        self, *, lat: float, lon: float, to_polars: Literal[False] = False
    ) -> List[PostCode]: ...

    def get_postcode(
        self, *, lat: float, lon: float, to_polars: bool = False
    ) -> pl.DataFrame | List[PostCode]:
        """Get the postcode for a specific lat/lon.

        Args:
            lat: The latitude.
            lon: The longitude.
            to_polars: Whether to return the data as a Polars DataFrame.
                Defaults to False.

        Returns:
            PostCode: The postcode.
        """
        validate_lat(lat)
        validate_lon(lon)

        params = {"lat": lat, "lon": lon}

        try:
            response = self.transport.request("GET", params=params)
        except HTTPStatusError as e:
            raise ValueError(
                f"Postcodes.io API error: {e.response.text}"
            ) from e

        # The API returns null or a list inside 'result'
        data = response.json().get("result") or []

        models = self._to_model_list(data, PostCode)
        return self._format(models, to_polars)
