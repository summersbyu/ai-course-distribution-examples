"""Safety checks for AI-generated SQL.

The app runs SQL that a model wrote, so it never trusts it:
  1. Only one statement, and it must be a SELECT (or a WITH ... SELECT).
  2. No keywords that change data or the database.
  3. The database is opened read-only, so even a missed case cannot write.
  4. Results are capped so a runaway query cannot flood the page.
"""
import re
import sqlite3
from pathlib import Path

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum|reindex|truncate|grant)\b",
    re.IGNORECASE,
)
MAX_ROWS = 500


class UnsafeSQL(ValueError):
    pass


def _strip_comments(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    return re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)


def check_sql(sql: str) -> str:
    """Return a cleaned single SELECT statement, or raise UnsafeSQL with a reason."""
    cleaned = _strip_comments(sql).strip().rstrip(";").strip()
    if not cleaned:
        raise UnsafeSQL("The query is empty.")
    if ";" in cleaned:
        raise UnsafeSQL("Only one SQL statement is allowed.")
    first = cleaned.split(None, 1)[0].lower()
    if first not in ("select", "with"):
        raise UnsafeSQL("Only SELECT queries are allowed.")
    hit = FORBIDDEN.search(cleaned)
    if hit:
        raise UnsafeSQL(f"The keyword '{hit.group(0).upper()}' is not allowed.")
    return cleaned


def run_readonly(db_path: Path, sql: str):
    """Run a checked query on a read-only connection. Returns (columns, rows, truncated)."""
    safe = check_sql(sql)
    uri = f"file:{db_path.resolve().as_posix()}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        cur = con.execute(safe)
        cols = [c[0] for c in cur.description or []]
        rows = cur.fetchmany(MAX_ROWS + 1)
    finally:
        con.close()
    return cols, rows[:MAX_ROWS], len(rows) > MAX_ROWS


def schema_text(db_path: Path) -> str:
    """The CREATE statements, which the model reads to write correct joins."""
    uri = f"file:{db_path.resolve().as_posix()}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        rows = con.execute("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    finally:
        con.close()
    return "\n\n".join(r[0] for r in rows)
