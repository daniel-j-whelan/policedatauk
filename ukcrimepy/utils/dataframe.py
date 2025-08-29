import polars as pl
from pydantic import BaseModel
from typing import List

from models import CrimeWithOutcomes, CrimeReport


def pydantic_to_df(model_list: List[BaseModel], sep="_") -> pl.DataFrame:
    """Converts a list of Pydantic models into a Polars DataFrame.

    Uses pl.DataFrame for flat data, pl.json_normalize for nested data.

    Args:
        model_list: A list of Pydantic models.

        sep: The separator to use when flattening the data.
            Defaults to "_".

    Returns:
        A Polars DataFrame.
    """
    df = pl.json_normalize(
        [model.model_dump(exclude_none=True, mode="json") for model in model_list],
        separator=sep,
    )
    return df


def crime_reports_to_df(crime_reports: List[CrimeReport]) -> pl.DataFrame:
    """Convert a list of CrimeReport models into a flattened Polars DataFrame.

    Args:
        crime_reports: A list of CrimeReport models.

    Returns:
        A Polars DataFrame with flattened data.
    """
    if isinstance(crime_reports, (CrimeReport,)):  # single object
        crime_list = [crime_reports]
    else:
        crime_list = crime_reports

    df = pydantic_to_df(crime_list)
    df = df.rename(
        {
            "location_latitude": "latitude",
            "location_longitude": "longitude",
            "location_street_id": "street_id",
            "location_street_name": "street_name",
            "outcome_status_category": "outcome_category",
            "outcome_status_date": "outcome_date",
        }
    )
    return df


def crimes_with_outcomes_to_df(
    cwo_input: list[CrimeWithOutcomes], id: str
) -> pl.DataFrame:
    """Convert a list of CrimeWithOutcomes models into a flattened Polars DataFrame.

    Args:
        cwo_input: A list of CrimeWithOutcomes models.

        id: The persistent_id of the crime report to filter by.

    Returns:
        A Polars DataFrame with flattened data.
    """
    if isinstance(cwo_input, (CrimeWithOutcomes,)):  # single object
        cwo_list = [cwo_input]
    else:
        cwo_list = cwo_input

    # Build a Polars DF
    df = pydantic_to_df(cwo_list)

    # Explode outcomes so each row = 1 outcome
    df = df.explode("outcomes")

    # Flatten nested dicts (crime.*, outcomes.*)
    df = pl.json_normalize(df.to_dicts(), separator="_")

    # Rename for clarity
    df = df.rename(
        {
            "crime_location_latitude": "latitude",
            "crime_location_longitude": "longitude",
            "crime_location_street_id": "street_id",
            "crime_location_street_name": "street_name",
            "outcomes_date": "outcome_date",
            "outcomes_category_name": "outcome_category_name",
            "outcomes_category_code": "outcome_category_code",
        }
    )

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
