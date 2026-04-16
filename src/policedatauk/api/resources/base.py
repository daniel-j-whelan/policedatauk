"""Base module for the policedatauk resources / endpoints."""

from typing import List, Type, TypeVar

import polars as pl
from pydantic import BaseModel

from ...utils import pydantic_to_df

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class BaseResource:
    """Base class for shared logic across all resources / endpoints."""

    def _to_model(
        self, data: dict, model_class: Type[PydanticModel]
    ) -> PydanticModel:
        """Standardise single object / model parsing and valiation."""
        return model_class.model_validate(data)

    def _to_model_list(
        self, data: list, model_class: Type[PydanticModel]
    ) -> List[PydanticModel]:
        """Standardise lists of objects / models parsing and valiation."""
        return [model_class.model_validate(item) for item in data]

    def _format(
        self, data: PydanticModel | List[PydanticModel], to_polars: bool
    ) -> PydanticModel | List[PydanticModel] | pl.DataFrame:
        """Conversion from model/s to Polars if requested."""
        if to_polars:
            items = data if isinstance(data, list) else [data]
            return pydantic_to_df(items)
        return data
