"""Utilities for working with Polars DataFrames."""

from typing import Dict, List, Optional

import polars as pl
from pydantic import BaseModel

RENAME_MAP = {
    "crime_reports": {
        "location_latitude": "latitude",
        "location_longitude": "longitude",
        "location_street_id": "street_id",
        "location_street_name": "street_name",
        "outcome_status_category": "outcome_category",
        "outcome_status_date": "outcome_date",
    },
    "crimes_with_outcomes": {
        "crime_location_latitude": "latitude",
        "crime_location_longitude": "longitude",
        "crime_location_street_id": "street_id",
        "crime_location_street_name": "street_name",
        "outcomes_date": "outcome_date",
        "outcomes_category_name": "outcome_name",
        "outcomes_category_code": "outcome_code",
    },
}


def pydantic_to_df(
    models: BaseModel | List[BaseModel],
    sep: str = "_",
    exclude_none: bool = True,
    explode: bool = True,
    rename: Optional[Dict[str, str]] = None,
    rename_key: Optional[str] = None,
) -> pl.DataFrame:
    """Converts Pydantic models into a Polars DataFrame.

    Handles nested dicts with pl.json_normalize and optionally explodes
    list-of-dicts into rows + flattens them.

    Args:
        models: Pydantic model/s.
        sep: Separator for flattened keys.
            Default is "_".
        exclude_none: Exclude fields containing Nones in model results.
        explode: Whether to explode list-of-dicts columns into seperate rows.
            Default is True.
        rename: Optional dict mapping old column names to new names.
        rename_key: Optional key to look up in RENAME_MAP for renaming.
            If provided, this will override the `rename` argument.

    Returns:
        A Polars DataFrame.
    """
    if isinstance(models, BaseModel):
        records = [models.model_dump(exclude_none=exclude_none, mode="json")]
    else:
        records = [
            model.model_dump(exclude_none=exclude_none, mode="json")
            for model in models
        ]
    df = pl.json_normalize(records, separator=sep)
    if explode:
        for col in df.columns:
            if df.schema[col] == pl.List(pl.Struct):
                df = df.explode(col).unnest(col)
    if rename_key:
        df = df.rename(RENAME_MAP.get(rename_key, {}), strict=False)
    elif rename:
        df = df.rename(rename, strict=False)

    df = clean_polars_df(df)
    return df


def handle_empty_strings(df: pl.DataFrame) -> pl.DataFrame:
    """Replace empty or whitespace-only strings in string columns with None.

    For each string column:
    - Strip leading/trailing whitespace.
    - If the stripped value is empty, replace with None.
    - Otherwise, keep the stripped value.

    Args:
        df: Polars DataFrame to clean.

    Returns:
        Cleaned DataFrame with empty/whitespace strings replaced by None.
    """
    string_columns = [
        column for column, dtype in df.schema.items() if dtype == pl.Utf8
    ]

    if not string_columns:
        return df

    df = df.with_columns(
        [
            pl.when(pl.col(column).str.strip_chars().str.len_chars() == 0)
            .then(None)
            .otherwise(pl.col(column).str.strip_chars())
            .alias(column)
            for column in string_columns
        ]
    )

    return df


def drop_empty_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Drop columns that are entirely null or empty after cleaning.

    Args:
        df: Polars DataFrame.

    Returns:
        DataFrame without all-null columns.
    """
    keep_cols = []
    for c in df.columns:
        all_null = df.select(pl.col(c).is_null().all()).to_series()[0]
        if not all_null:
            keep_cols.append(c)
    return df.select(keep_cols)


def drop_empty_rows(df: pl.DataFrame) -> pl.DataFrame:
    """Drop rows that are entirely null across all columns.

    Args:
        df: Polars DataFrame.

    Returns:
        DataFrame without all-null rows.
    """
    not_null_exprs = [pl.col(column).is_not_null() for column in df.columns]
    any_not_null = pl.any_horizontal(not_null_exprs)

    return df.filter(any_not_null)


def parse_datetime_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Parse datetime columns from a Polars DataFrame.

    Only parse columns with the exact names "date", "datetime", or "timestamp".
    The datetime columns are expected to be in ISO 8601 format, with the exact
    format string: "%d-%m-%YT%H:%M:%SZ".

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with datetime columns parsed.
    """

    return df.with_columns(
        [
            pl.col(col).str.strptime(pl.Datetime, "%Y-%m")
            for col, dtype in df.schema.items()
            if col in ["date", "month", "timestamp"]
        ]
    )


def clean_polars_df(df: pl.DataFrame) -> pl.DataFrame:
    """
    Clean a Polars DataFrame from JSON API response data.

    - Drop fully null columns
    - Drop string columns with only empty values
    - Strip whitespace from string columns
    - Parse ISO datetime columns (if named 'date', 'datetime', or 'timestamp')
    - Drop rows with no meaningful data

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with cleaned data.
    """
    return (
        df.pipe(handle_empty_strings)
        .pipe(drop_empty_columns)
        .pipe(drop_empty_rows)
        .pipe(parse_datetime_columns)
    )
