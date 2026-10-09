"""Build the synthetic Summit Outfitters database used by the SQL analyst.

All names and amounts are generated. Nothing here is real company or personal data.
Run:  python build_db.py   (writes data/summit_outfitters.db)
"""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

random.seed(407)
DB = Path(__file__).parent / "data" / "summit_outfitters.db"

SCHEMA = """
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region        TEXT NOT NULL,          -- West, Mountain, Central, East
    credit_limit  REAL NOT NULL
);
CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    product_name  TEXT NOT NULL,
    category      TEXT NOT NULL,          -- Apparel, Footwear, Camping, Climbing
    unit_cost     REAL NOT NULL,
    list_price    REAL NOT NULL
);
CREATE TABLE sales_invoices (
    invoice_id    INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    invoice_date  TEXT NOT NULL,          -- YYYY-MM-DD
    due_date      TEXT NOT NULL,
    status        TEXT NOT NULL           -- Paid, Open, Void
);
CREATE TABLE invoice_lines (
    line_id       INTEGER PRIMARY KEY,
    invoice_id    INTEGER NOT NULL REFERENCES sales_invoices(invoice_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL,
    unit_price    REAL NOT NULL
);
CREATE TABLE cash_receipts (
    receipt_id    INTEGER PRIMARY KEY,
    invoice_id    INTEGER NOT NULL REFERENCES sales_invoices(invoice_id),
    receipt_date  TEXT NOT NULL,
    amount        REAL NOT NULL
);
CREATE TABLE vendors (
    vendor_id     INTEGER PRIMARY KEY,
    vendor_name   TEXT NOT NULL,
    category      TEXT NOT NULL           -- Inventory, Freight, Utilities, Services
);
CREATE TABLE vendor_bills (
    bill_id       INTEGER PRIMARY KEY,
    vendor_id     INTEGER NOT NULL REFERENCES vendors(vendor_id),
    bill_date     TEXT NOT NULL,
    due_date      TEXT NOT NULL,
    amount        REAL NOT NULL,
    approved_by   TEXT,                   -- NULL means not yet approved
    paid_date     TEXT                    -- NULL means unpaid
);
"""

REGIONS = ["West", "Mountain", "Central", "East"]
CUST_WORDS = ["Alpine", "Ridge", "Canyon", "Summit", "Trail", "Basecamp", "Peak", "Timber", "River", "Mesa"]
CUST_SUFFIX = ["Outdoor Co.", "Sports", "Supply", "Gear Shop", "Adventures"]
PRODUCTS = [
    ("Trail Runner Shoe", "Footwear", 48, 120), ("Hiking Boot", "Footwear", 70, 175),
    ("Rain Shell Jacket", "Apparel", 55, 149), ("Fleece Pullover", "Apparel", 22, 69),
    ("Merino Base Layer", "Apparel", 30, 89), ("2-Person Tent", "Camping", 120, 299),
    ("Sleeping Bag 20F", "Camping", 75, 189), ("Camp Stove", "Camping", 28, 79),
    ("Climbing Harness", "Climbing", 32, 85), ("Dynamic Rope 60m", "Climbing", 110, 249),
    ("Chalk Bag", "Climbing", 6, 22), ("Headlamp", "Camping", 12, 39),
]
VENDORS = [
    ("Wasatch Textiles", "Inventory"), ("Granite Footwear Mfg", "Inventory"), ("Pioneer Camp Goods", "Inventory"),
    ("Crux Climbing Supply", "Inventory"), ("Beehive Freight", "Freight"), ("Canyon Logistics", "Freight"),
    ("Provo Power & Light", "Utilities"), ("Uinta IT Services", "Services"), ("Bonneville Cleaning", "Services"),
]
APPROVERS = ["J. Larsen", "M. Ortiz", "K. Chen"]


def d(s: date) -> str:
    return s.isoformat()


def main() -> None:
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    names = set()
    customers = []
    while len(customers) < 40:
        n = f"{random.choice(CUST_WORDS)} {random.choice(CUST_SUFFIX)}"
        if n in names:
            continue
        names.add(n)
        customers.append((len(customers) + 1, n, random.choice(REGIONS), random.choice([5000, 10000, 25000, 50000])))
    con.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)
    con.executemany("INSERT INTO products VALUES (?,?,?,?,?)",
                    [(i + 1, *p) for i, p in enumerate(PRODUCTS)])
    con.executemany("INSERT INTO vendors VALUES (?,?,?)", [(i + 1, *v) for i, v in enumerate(VENDORS)])

    start, today = date(2026, 1, 1), date(2026, 9, 30)
    line_id = receipt_id = 0
    for inv_id in range(1, 601):
        cust = random.choice(customers)
        inv_date = start + timedelta(days=random.randint(0, (today - start).days))
        due = inv_date + timedelta(days=30)
        status = "Void" if random.random() < 0.02 else ("Open" if due > today - timedelta(days=random.randint(0, 90)) and random.random() < 0.35 else "Paid")
        con.execute("INSERT INTO sales_invoices VALUES (?,?,?,?,?)", (inv_id, cust[0], d(inv_date), d(due), status))
        total = 0.0
        for _ in range(random.randint(1, 4)):
            line_id += 1
            p = random.choice(PRODUCTS)
            pid = PRODUCTS.index(p) + 1
            qty = random.randint(1, 12)
            price = round(p[3] * random.choice([1, 1, 1, 0.9, 0.85]), 2)  # occasional discounts
            total += qty * price
            con.execute("INSERT INTO invoice_lines VALUES (?,?,?,?,?)", (line_id, inv_id, pid, qty, price))
        if status == "Paid":
            receipt_id += 1
            pay = inv_date + timedelta(days=random.randint(5, 55))
            # a few short payments create reconciling differences worth finding
            amt = round(total if random.random() > 0.04 else total - random.choice([10, 25, 50]), 2)
            con.execute("INSERT INTO cash_receipts VALUES (?,?,?,?)", (receipt_id, inv_id, d(min(pay, today)), amt))

    for bill_id in range(1, 301):
        v = random.randint(1, len(VENDORS))
        bdate = start + timedelta(days=random.randint(0, (today - start).days))
        amt = round(random.uniform(200, 18000), 2)
        approver = None if random.random() < 0.06 else random.choice(APPROVERS)  # control exceptions
        paid = d(bdate + timedelta(days=random.randint(10, 45))) if random.random() < 0.8 else None
        if paid and paid > d(today):
            paid = None
        con.execute("INSERT INTO vendor_bills VALUES (?,?,?,?,?,?,?)",
                    (bill_id, v, d(bdate), d(bdate + timedelta(days=30)), amt, approver, paid))
    # a handful of duplicate-looking bills for students to discover
    for src in random.sample(range(1, 301), 4):
        row = con.execute("SELECT vendor_id, bill_date, due_date, amount, approved_by, paid_date FROM vendor_bills WHERE bill_id=?", (src,)).fetchone()
        con.execute("INSERT INTO vendor_bills (vendor_id,bill_date,due_date,amount,approved_by,paid_date) VALUES (?,?,?,?,?,?)", row)

    con.commit()
    for t in ["customers", "products", "sales_invoices", "invoice_lines", "cash_receipts", "vendors", "vendor_bills"]:
        print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    con.close()


if __name__ == "__main__":
    main()
