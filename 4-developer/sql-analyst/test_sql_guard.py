"""Run with:  python -m pytest test_sql_guard.py   (or just: python test_sql_guard.py)"""
from pathlib import Path

from sql_guard import UnsafeSQL, check_sql, run_readonly

DB = Path(__file__).parent / "data" / "summit_outfitters.db"

ALLOWED = [
    "SELECT COUNT(*) FROM customers",
    "with t as (select 1 as x) select x from t;",
    "-- comment\nSELECT region FROM customers",
]
BLOCKED = [
    "DELETE FROM customers",
    "SELECT 1; DROP TABLE customers",
    "UPDATE vendor_bills SET approved_by='me'",
    "PRAGMA table_info(customers)",
    "ATTACH DATABASE 'x.db' AS x",
    "",
]


def test_allowed():
    for sql in ALLOWED:
        check_sql(sql)


def test_blocked():
    for sql in BLOCKED:
        try:
            check_sql(sql)
        except UnsafeSQL:
            continue
        raise AssertionError(f"should have been blocked: {sql!r}")


def test_readonly_query_runs():
    cols, rows, truncated = run_readonly(DB, "SELECT region, COUNT(*) FROM customers GROUP BY region")
    assert cols == ["region", "COUNT(*)"] and rows and not truncated


if __name__ == "__main__":
    test_allowed(); test_blocked(); test_readonly_query_runs()
    print("All SQL guard tests passed.")
