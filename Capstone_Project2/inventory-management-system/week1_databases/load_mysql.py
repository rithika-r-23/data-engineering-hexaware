
import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
load_dotenv(ROOT / ".env")

TABLES = {  
    "suppliers": ("suppliers.csv", ["supplier_id", "supplier_name", "contact_person", "email", "phone", "city"]),
    "warehouses": ("warehouses.csv", ["warehouse_id", "warehouse_name", "city", "state", "capacity_units"]),
    "products": ("products.csv", ["product_id", "sku", "product_name", "category", "unit_price", "supplier_id",
                                  "reorder_level", "max_stock_level", "reorder_quantity", "is_active"]),
    "stock_movements": ("stock_movements.csv", ["movement_id", "product_id", "warehouse_id", "movement_type",
                                                "quantity", "movement_date", "reference_no", "reason"]),
}


def insert(cur, table, df, batch=1000):
    cols = list(df.columns)
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
    rows = df.astype(object).where(df.notna(), None).values.tolist()
    for i in range(0, len(rows), batch):
        cur.executemany(sql, rows[i:i + batch])
    print(f"  {table:<16}{len(rows):>8,} rows")


def main():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"), port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"), password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "inventory_db"))
    cur = conn.cursor()
    try:
        print("Clearing old data ...")
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for t in ["stock_levels", "stock_movements", "products", "warehouses", "suppliers"]:
            cur.execute(f"TRUNCATE TABLE {t}")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        print("Loading CSV files ...")
        for table, (csv_name, cols) in TABLES.items():
            insert(cur, table, pd.read_csv(RAW / csv_name)[cols])
        conn.commit()

        cur.execute("SELECT COUNT(*), COALESCE(SUM(quantity_on_hand), 0), COALESCE(MIN(quantity_on_hand), 0) FROM stock_levels")
        n, total, lowest = cur.fetchone()
        print(f"\nstock_levels rows: {n}  |  total units: {total:,}  |  lowest level: {lowest}")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
    print("Done. Now run 02_crud_operations.sql, 03_stored_procedures.sql and 04_indexes.sql")


if __name__ == "__main__":
    main()
