import polars as pl
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

def handle_empty_strings(df: pl.DataFrame) -> pl.DataFrame:
    """Handle empty strings in a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame.

    Returns:
        DataFrame with empty strings handled.
    """
    return df.with_columns([
        pl.col(col).str.strip_chars().replace("", None)
        for col, dtype in df.schema.items() if dtype == pl.String
    ])

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
    
    return df.with_columns([
        pl.col(col).str.strptime(pl.Datetime, "%Y-%m")
        for col, dtype in df.schema.items() if col in ["date", "month", "timestamp"]
    ])

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
        df
        .pipe(handle_empty_strings)
        .pipe(drop_empty_columns)
        .pipe(drop_empty_rows)
        .pipe(parse_datetime_columns)
    )
