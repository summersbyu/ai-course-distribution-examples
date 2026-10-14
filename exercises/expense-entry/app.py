from pathlib import Path
import sqlite3
import streamlit as st

DB = Path(__file__).parent / "expenses.db"

def connect():
    return sqlite3.connect(DB)

with connect() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            expense_date TEXT NOT NULL,
            vendor TEXT NOT NULL,
            category TEXT NOT NULL,
            amount_cents INTEGER NOT NULL CHECK(amount_cents > 0)
        )
    """)

st.title("Expense Entry")
st.caption("Practice with fictional expenses only.")

with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date")
    vendor = st.text_input("Vendor")
    category = st.selectbox(
        "Category", ["Office supplies", "Travel", "Meals", "Software"]
    )
    amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
    submitted = st.form_submit_button("Save expense")

    if submitted:
        if not vendor.strip():
            st.error("Enter a vendor.")
        else:
            with connect() as conn:
                conn.execute(
                    """INSERT INTO expenses
                       (expense_date, vendor, category, amount_cents)
                       VALUES (?, ?, ?, ?)""",
                    (date.isoformat(), vendor.strip(), category,
                     int(round(amount * 100))),
                )
            st.success("Expense saved to SQLite.")

st.subheader("Saved expenses")
with connect() as conn:
    cursor = conn.execute("""
        SELECT id, expense_date AS date, vendor, category,
               amount_cents / 100.0 AS amount
        FROM expenses
        ORDER BY id DESC
    """)
    columns = [column[0] for column in cursor.description]
    records = [dict(zip(columns, row)) for row in cursor.fetchall()]

if records:
    st.dataframe(records, hide_index=True)
else:
    st.info("Save your first expense above.")

st.caption(f"Database location: {DB}")

# SQL practice area
import time
import pandas as pd

st.divider()
st.subheader("SQL practice")
st.caption(
    "Table: expenses | Columns: id, expense_date, vendor, "
    "category, amount_cents. Amounts are stored in cents."
)

with st.form("sql_form"):
    sql = st.text_area(
        "Write a query",
        value="""SELECT category,
       COUNT(*) AS expense_count,
       SUM(amount_cents) / 100.0 AS total_dollars
FROM expenses
GROUP BY category
ORDER BY total_dollars DESC;""",
        height=180,
    )
    run_query = st.form_submit_button("Run query")

def allow_query(action, arg1, arg2, database, source):
    if action == sqlite3.SQLITE_READ:
        return (
            sqlite3.SQLITE_OK
            if arg1 == "expenses"
            else sqlite3.SQLITE_DENY
        )
    if action in (
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    ):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY

if run_query:
    query_conn = None
    try:
        query_conn = sqlite3.connect(
            DB.resolve().as_uri() + "?mode=ro", uri=True
        )
        query_conn.set_authorizer(allow_query)
        deadline = time.monotonic() + 3
        query_conn.set_progress_handler(
            lambda: int(time.monotonic() > deadline), 1000
        )

        cursor = query_conn.execute(sql)
        rows = cursor.fetchmany(501)
        columns = [item[0] for item in cursor.description]
        st.dataframe(
            pd.DataFrame(rows[:500], columns=columns),
            hide_index=True,
        )
        if len(rows) > 500:
            st.info("Showing only the first 500 rows.")
        else:
            st.caption(f"{len(rows)} row(s) returned.")
    except sqlite3.Error as error:
        st.error(
            f"Query could not run: {error}. "
            "Use one read-only query against expenses."
        )
    finally:
        if query_conn is not None:
            query_conn.close()
