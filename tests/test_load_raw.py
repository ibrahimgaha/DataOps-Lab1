import duckdb
import pandas as pd
import pytest

import load_raw


@pytest.fixture
def warehouse(tmp_path, monkeypatch):
    sample = tmp_path / "orders.csv"
    sample.write_text(
        "order_id,order_date,customer_id,country,product,quantity,unit_price\n"
        "1,2026-10-05,,Tunisia,Mouse,1,19.90\n"
        "2,2026-10-05,C001,Italy,Keyboard,2,45.00\n",
        encoding="utf-8",
    )
    path = tmp_path / "warehouse.duckdb"
    monkeypatch.setattr(load_raw, "WAREHOUSE", path)
    assert load_raw.main(str(sample)) == 0
    return path, sample


def test_load_accepts_a_missing_customer(warehouse):
    path, _ = warehouse
    with duckdb.connect(str(path), read_only=True) as connection:
        assert connection.execute("select count(*) from raw.orders").fetchone() == (2,)
        assert connection.execute(
            "select customer_id from raw.orders where order_id = '1'"
        ).fetchone() == (None,)


@pytest.mark.parametrize("problem", ["prices_in_cents", "renamed_price"])
def test_load_refuses_invalid_file_and_keeps_raw_orders(problem, warehouse, tmp_path):
    path, sample = warehouse
    orders = pd.read_csv(sample)
    if problem == "prices_in_cents":
        orders["unit_price"] *= 100
    else:
        orders = orders.rename(columns={"unit_price": "price"})
    bad_file = tmp_path / "bad_orders.csv"
    orders.to_csv(bad_file, index=False)

    assert load_raw.main(str(bad_file)) == 1
    with duckdb.connect(str(path), read_only=True) as connection:
        assert connection.execute(
            "select distinct _source_file from raw.orders"
        ).fetchall() == [(str(sample),)]
