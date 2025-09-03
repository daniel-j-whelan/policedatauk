import polars as pl
from pydantic import BaseModel
from typing import List, Dict, Optional

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
        "outcomes_category_name": "outcome_category",
        "outcomes_category_code": "outcome_code",
    }
}
def pydantic_to_df(
    models: BaseModel | List[BaseModel],
    sep: str = "_",
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
        explode: Whether to explode list-of-dicts columns into seperate rows.
            Default is True.
        rename: Optional dict mapping old column names to new names.
        rename_key: Optional key to look up in RENAME_MAP for renaming.
            If provided, this will override the `rename` argument.

    Returns:
        A Polars DataFrame.
    """
    if isinstance(models, BaseModel):
        records = [models.model_dump(exclude_none=True, mode="json")]
    else:
        records = [model.model_dump(exclude_none=True, mode="json") for model in models]
    df = pl.json_normalize(records, separator=sep)
    if explode:
        for col in df.columns:
            if df.schema[col] == pl.List(pl.Struct):
                df = df.explode(col).unnest(col)
    if rename_key:
        df = df.rename(RENAME_MAP.get(rename_key, {}))
    elif rename:
        df = df.rename(rename)
    return df

def handle_empty_strings(df: pl.DataFrame) -> pl.DataFrame:
    """Handle empty strings in a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with empty strings handled.
    """
    return df.with_columns(
        [
            pl.col(col).str.strip_chars().replace("", None)
            for col, dtype in df.schema.items()
            if dtype == pl.String
        ]
    )


def drop_empty_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Drop fully empty columns from a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with fully empty columns dropped.
    """
    return df.drop(pl.all().is_empty())


def drop_empty_rows(df: pl.DataFrame) -> pl.DataFrame:
    """Drop fully null rows from a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with fully null rows dropped.
    """
    return df.drop_nulls(how="all")


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
