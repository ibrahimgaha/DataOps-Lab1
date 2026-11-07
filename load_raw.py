"""Load a daily orders CSV into DuckDB without cleaning the source values."""

import argparse
from pathlib import Path

import duckdb

WAREHOUSE = Path(__file__).with_name("warehouse.duckdb")


def main(path):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Path to the daily orders CSV")
    main(parser.parse_args().csv)
