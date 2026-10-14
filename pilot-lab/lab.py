"""Persistence and bounded read-only SQL for a synthetic accounting lab."""
from contextlib import closing
import csv
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import io
import json
import os
from pathlib import Path
import sqlite3
import time
import uuid

VERSION = "1.0"
CATEGORIES = ("Office supplies", "Travel", "Meals", "Software")
DB_PATH = Path(os.environ.get("ACCOUNTING_LAB_DB", str(Path(__file__).resolve().parent.parent / ".lab-data" / "expenses.db")))
MAX_ROWS = 500
MAX_SECONDS = 3
FUNCTIONS = {"sum", "total", "count", "avg", "min", "max", "round", "abs", "coalesce", "ifnull", "nullif", "lower", "upper", "length", "trim", "substr", "substring", "date", "strftime", "typeof", "like"}

def connection():
    return sqlite3.connect(DB_PATH, timeout=5)

def initialize():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(connection()) as con, con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS expenses (
          id INTEGER PRIMARY KEY,
          expense_date TEXT NOT NULL,
          vendor TEXT NOT NULL,
          category TEXT NOT NULL,
          amount_cents INTEGER NOT NULL CHECK(amount_cents > 0)
        );
        CREATE TABLE IF NOT EXISTS lab_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS query_runs (
          id INTEGER PRIMARY KEY, run_at TEXT NOT NULL, sql TEXT NOT NULL,
          prediction TEXT NOT NULL, columns_json TEXT NOT NULL,
          rows_json TEXT NOT NULL, truncated INTEGER NOT NULL
        );
        """)
        con.execute("INSERT OR IGNORE INTO lab_meta VALUES ('lab_id', ?)", (uuid.uuid4().hex[:8],))

def meta(key, default=""):
    with closing(connection()) as con:
        found = con.execute("SELECT value FROM lab_meta WHERE key=?", (key,)).fetchone()
    return found[0] if found else default

def save_meta(key, value):
    with closing(connection()) as con, con:
        con.execute("INSERT INTO lab_meta VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))

def cents(value):
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount <= 0 or amount > Decimal("1000000"):
            raise ValueError("Enter an amount from $0.01 to $1,000,000.00.")
        if amount != amount.quantize(Decimal("0.01")):
            raise ValueError("Use no more than two decimal places.")
        return int(amount * 100)
    except InvalidOperation:
        raise ValueError("Enter a valid dollar amount.") from None

def add_expense(expense_date, vendor, category, amount):
    date.fromisoformat(str(expense_date))
    vendor = vendor.strip()
    if not vendor or len(vendor) > 100:
        raise ValueError("Enter a vendor name between 1 and 100 characters.")
    if category not in CATEGORIES:
        raise ValueError("Choose one of the listed categories.")
    with closing(connection()) as con, con:
        cur = con.execute("INSERT INTO expenses (expense_date, vendor, category, amount_cents) VALUES (?, ?, ?, ?)", (str(expense_date), vendor, category, cents(amount)))
        return cur.lastrowid

def expenses():
    with closing(connection()) as con:
        return con.execute("SELECT id, expense_date, vendor, category, amount_cents FROM expenses ORDER BY id").fetchall()

def summary():
    with closing(connection()) as con:
        return con.execute("SELECT COUNT(*), COALESCE(SUM(amount_cents),0) FROM expenses").fetchone()

def authorize(action, arg1, arg2, database, source):
    if action == sqlite3.SQLITE_READ:
        return sqlite3.SQLITE_OK if arg1 == "expenses" and database == "main" else sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_FUNCTION:
        return sqlite3.SQLITE_OK if (arg2 or "").lower() in FUNCTIONS else sqlite3.SQLITE_DENY
    if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_RECURSIVE):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY

def query(sql, prediction="", record=True, seconds=MAX_SECONDS):
    if not sql.strip():
        raise ValueError("Write a SELECT query before choosing Run query.")
    if len(sql) > 12000:
        raise ValueError("Keep this practice query under 12,000 characters.")
    with closing(sqlite3.connect(DB_PATH.resolve().as_uri() + "?mode=ro", uri=True, timeout=3)) as con:
        con.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1000000)
        con.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 12000)
        con.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 50)
        con.set_authorizer(authorize)
        deadline = time.monotonic() + seconds
        con.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
        try:
            cursor = con.execute(sql)
            if cursor.description is None:
                raise ValueError("Use a SELECT query that returns a table.")
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchmany(MAX_ROWS + 1)
        except sqlite3.Error as exc:
            message = str(exc)
            if message == "interrupted":
                raise ValueError("The query exceeded the time limit. Simplify it and try again.") from None
            if "authorized" in message or "prohibited" in message:
                raise ValueError("The SQL editor only permits reading expenses with supported SQL functions. Your saved expenses were not changed.") from None
            raise ValueError(f"SQL could not run: {message}") from None
    truncated = len(rows) > MAX_ROWS
    rows = rows[:MAX_ROWS]
    if record:
        with closing(connection()) as con, con:
            con.execute("INSERT INTO query_runs (run_at,sql,prediction,columns_json,rows_json,truncated) VALUES (?,?,?,?,?,?)", (datetime.now(timezone.utc).isoformat(), sql, prediction.strip(), json.dumps(columns), json.dumps(rows), int(truncated)))
    return columns, rows, truncated

def export_csv():
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(["id", "expense_date", "vendor", "category", "amount_cents"])
    writer.writerows(expenses())
    return buffer.getvalue().encode("utf-8")

def restore_csv(content):
    if len(content) > 1000000:
        raise ValueError("Use a lab CSV backup smaller than 1 MB.")
    try:
        reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
        if reader.fieldnames != ["id", "expense_date", "vendor", "category", "amount_cents"]:
            raise ValueError("Choose the expense CSV downloaded from this lab.")
        records = []
        ids = set()
        for row in reader:
            if len(records) >= 1000 or None in row:
                raise ValueError("Backup must contain at most 1,000 valid records.")
            identifier = int(row["id"])
            amount = int(row["amount_cents"])
            if identifier <= 0 or identifier in ids or not 1 <= amount <= 100000000:
                raise ValueError("Backup contains invalid IDs or amounts.")
            date.fromisoformat(row["expense_date"])
            vendor = row["vendor"].strip()
            if not vendor or len(vendor) > 100 or row["category"] not in CATEGORIES:
                raise ValueError("Backup contains an invalid vendor or category.")
            ids.add(identifier)
            records.append((identifier, row["expense_date"], vendor, row["category"], amount))
    except (UnicodeError, csv.Error, TypeError, KeyError):
        raise ValueError("This file is not a valid lab CSV backup.") from None
    with closing(connection()) as con, con:
        con.execute("BEGIN IMMEDIATE")
        if con.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]:
            raise ValueError("Restore is available only in an empty lab. Reopen your original workspace if it already has expenses.")
        if not records:
            raise ValueError("The backup contains no expenses.")
        con.executemany("INSERT INTO expenses VALUES (?,?,?,?,?)", records)
    return len(records)

def save_checkpoint():
    count, total = summary()
    save_meta("checkpoint", json.dumps({"count": count, "cents": total}))
    return count, total

def evidence():
    count, total = summary()
    lines = ["# Accounting Lab 01 evidence", "", f"Lab version: {VERSION}", f"Lab ID: {meta('lab_id')}", f"Workspace: {os.environ.get('CODESPACE_NAME', 'local practice')}", f"Exported UTC: {datetime.now(timezone.utc).isoformat()}", f"Expense count: {count}", f"Total dollars: {total / 100:.2f}", "", "## Saved query runs"]
    with closing(connection()) as con:
        runs = con.execute("SELECT run_at,sql,prediction,columns_json,rows_json,truncated FROM query_runs ORDER BY id").fetchall()
    for number, (stamp, sql, prediction, columns, rows, truncated) in enumerate(runs, 1):
        lines += ["", f"### Query {number}", f"Run UTC: {stamp}", f"Prediction: {prediction or 'Not recorded'}", "```sql", sql, "```", "Result columns: " + ", ".join(json.loads(columns)), "```text", json.dumps(json.loads(rows), indent=2), "```", f"Result truncated: {bool(truncated)}"]
    lines += ["", "## Reflection", meta("reflection", "Not recorded"), "", "## Restart observation", meta("restart_observation", "Not recorded"), "", "## Checkpoint saved before stopping", meta("checkpoint", "Not recorded")]
    return "\n".join(lines).encode("utf-8")
