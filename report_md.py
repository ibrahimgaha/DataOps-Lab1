"""Print the revenue report and optionally check its expected total."""

import argparse
from decimal import Decimal

import duckdb

from load_raw import WAREHOUSE


def main(expected=None):
    """Print the revenue report and check the optional total."""
    with duckdb.connect(str(WAREHOUSE), read_only=True) as connection:
        rows = connection.execute(
            "select country, revenue from revenue_by_country order by country"
        ).fetchall()
    total = sum((revenue for _, revenue in rows), Decimal("0.00"))

    print("| Country | Revenue |")
    print("| --- | ---: |")
    for country, revenue in rows:
        print(f"| {country} | {revenue:.2f} |")
    print(f"\n**Total: {total:.2f}**")

    if expected is not None and total != expected:
        print(f"\nREGRESSION: expected {expected:.2f}, got {total:.2f}")
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", nargs="?", type=Decimal, help="Expected total revenue for the report")
    raise SystemExit(main(parser.parse_args().expected))
