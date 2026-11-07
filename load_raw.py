"""Validate a daily orders CSV before loading its raw values into DuckDB."""

import argparse
from pathlib import Path

import duckdb
import pandas as pd
from pandera.errors import SchemaErrors

from pipeline.schema import RAW_ORDERS

WAREHOUSE = Path(__file__).with_name("warehouse.duckdb")


def main(path):
    try:
        RAW_ORDERS.validate(pd.read_csv(path, dtype=str), lazy=True)
    except SchemaErrors as error:
        print(f"REFUSED: {path} does not match the expected schema")
        print(error.failure_cases[["column", "check", "failure_case"]].to_string(index=False))
        return 1
    except (OSError, UnicodeError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        print(f"REFUSED: cannot read {path}: {error}")
        return 1

    with duckdb.connect(str(WAREHOUSE)) as connection:
        connection.execute("create schema if not exists raw")
        connection.execute(
            """
            create or replace table raw.orders as
            select
                *,
                row_number() over () as _row_number,
                ? as _source_file,
                current_timestamp as _loaded_at
            from read_csv(?, header = true, all_varchar = true)
            """,
            [path, path],
        )
        row_count = connection.execute("select count(*) from raw.orders").fetchone()[0]
    print(f"Loaded {row_count} rows from {path} into raw.orders")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Path to the daily orders CSV")
    raise SystemExit(main(parser.parse_args().csv))
