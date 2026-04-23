import pandas as pd
import mysql.connector
from mysql.connector import Error

# ── CONNECT ──────────────────────────────────────────────
try:
    conn = mysql.connector.connect(
        host     = "localhost",
        user     = "root",
        password = "your_password_here",  # password
        database = "superstore"
    )
    if conn.is_connected():
        print("✅ Connected to MySQL successfully")
except Error as e:
    print("❌ Connection failed:", e)
    exit()

# ── LOAD CSV ─────────────────────────────────────────────
df = pd.read_csv("data/processed/sales_cleaned.csv")
print("CSV loaded. Shape:", df.shape)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Columns:", df.columns.tolist())

# ── CREATE TABLE ─────────────────────────────────────────
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS sales")

create_table = """
CREATE TABLE sales (
    order_id        VARCHAR(50),
    order_date      DATE,
    ship_date       DATE,
    ship_mode       VARCHAR(50),
    customer_name   VARCHAR(100),
    segment         VARCHAR(50),
    state           VARCHAR(100),
    country         VARCHAR(100),
    market          VARCHAR(50),
    region          VARCHAR(50),
    product_id      VARCHAR(50),
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    product_name    VARCHAR(255),
    sales           DECIMAL(10,2),
    quantity        INT,
    discount        DECIMAL(5,3),
    profit          DECIMAL(10,2),
    shipping_cost   DECIMAL(10,2),
    order_priority  VARCHAR(20),
    year            INT,
    order_month     VARCHAR(20),
    order_year      INT,
    order_day       VARCHAR(20),
    shipping_days   INT
)
"""
cursor.execute(create_table)
print("✅ Table created")

# ── INSERT DATA ──────────────────────────────────────────
df   = df.where(pd.notnull(df), None)
cols = ", ".join(df.columns)
vals = ", ".join(["%s"] * len(df.columns))
insert = f"INSERT INTO sales ({cols}) VALUES ({vals})"
rows   = [tuple(row) for row in df.itertuples(index=False, name=None)]

batch_size = 1000
total      = len(rows)

for i in range(0, total, batch_size):
    batch = rows[i : i + batch_size]
    cursor.executemany(insert, batch)
    conn.commit()
    print(f"  Inserted rows {i} to {min(i+batch_size, total)} of {total}")

print(f"✅ All {total} rows inserted")

# ── VERIFY ───────────────────────────────────────────────
cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]
print(f"✅ Verified: {count} rows in MySQL")

cursor.close()
conn.close()
print("✅ Done. Connection closed")