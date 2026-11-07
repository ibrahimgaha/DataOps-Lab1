"""Run a SQL query against the local warehouse in read-only mode."""

import argparse
import sys

import duckdb

from load_raw import WAREHOUSE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sql", help="SQL query in quotes")
    args = parser.parse_args()
    # DuckDB draws its result table with Unicode borders.
    sys.stdout.reconfigure(encoding="utf-8")
    with duckdb.connect(str(WAREHOUSE), read_only=True) as connection:
        connection.sql(args.sql).show()
