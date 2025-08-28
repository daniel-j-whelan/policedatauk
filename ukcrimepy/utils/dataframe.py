import polars as pl
from collections.abc import MutableMapping
from models.crime import CrimeWithOutcomes
from typing import Dict, List, Any


def json_to_df(json_data: Dict[str, Any]) -> pl.DataFrame:
    """Converts a list of JSON objects into a Polars DataFrame.

    Uses pl.DataFrame for flat data, pl.json_normalize for nested data.

    Args:
        json_data (Dict[str, Any]): A JSON object.

    Returns:
        A Polars DataFrame.
    """
    if not json_data:
        return pl.DataFrame()

    # Check if any top-level values are nested
    nested = any(isinstance(k, (Dict, List)) for k in json_data.keys())

    if nested:
        return pl.json_normalize(json_data)
    else:
        return pl.DataFrame(json_data)


def flatten_dict(d: MutableMapping, parent_key: str = "", sep: str = "_") -> dict:
    """Recursively flattens a nested dictionary.

    Args:
        d: The dictionary to flatten.

        parent_key: The base key string for the current level of recursion.
            Defaults to an empty string.

        sep: The separator to use between keys.
            Defaults to "_".

    Example:
        {"a": {"b": 1, "c": 2}} -> {"a_b": 1, "a_c": 2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def crime_reports_to_polars(crime_reports: list, sep: str = "_") -> pl.DataFrame:
    """Convert a list of CrimeReport models into a flattened Polars DataFrame.

    Args:
        crime_reports: A list of CrimeReport models.

        sep: The separator to use between keys.
            Defaults to "_".

    Returns:
        A Polars DataFrame with flattened data.
    """
    records = [flatten_dict(crime.dict(), sep=sep) for crime in crime_reports]
    df = pl.DataFrame(records)
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


def crimes_with_outcomes_to_polars(
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

    rows = []
    for cwo in cwo_list:
        crime_dict = flatten_dict(cwo.crime.dict(), sep="_")
        for outcome in cwo.outcomes:
            row = crime_dict | flatten_dict(outcome.dict(), sep="_")
            rows.append(row)
    df = pl.DataFrame(rows)
    df = df.rename(
        {
            "location_latitude": "latitude",
            "location_longitude": "longitude",
            "location_street_id": "street_id",
            "location_street_name": "street_name",
            "date": "outcome_date",
        }
    )
    df = df.with_columns(persistent_id=pl.lit(id))
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
