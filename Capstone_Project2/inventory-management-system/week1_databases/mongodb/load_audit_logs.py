

import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pymongo import ASCENDING, DESCENDING, MongoClient

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

STAFF = ["meena.s", "ravi.k", "arjun.p", "divya.n", "karthik.r", "lakshmi.v"]
CATEGORY = {"Damaged goods": "DAMAGE", "Cycle count correction": "COUNT_CORRECTION",
            "Expired / obsolete stock": "EXPIRY", "Customer return": "RETURN",
            "Theft / shrinkage": "LOSS", "Found stock during audit": "COUNT_CORRECTION"}


def build_documents():
    df = pd.read_csv(ROOT / "data" / "raw" / "stock_movements.csv", parse_dates=["movement_date"])
    df = df.sort_values(["movement_date", "movement_id"])
    df["new_quantity"] = df.groupby(["product_id", "warehouse_id"])["quantity"].cumsum()
    df["previous_quantity"] = df["new_quantity"] - df["quantity"]
    adj = df[df["movement_type"] == "ADJUSTMENT"].copy()

    rng = np.random.default_rng(7)
    adj["performed_by"] = rng.choice(STAFF, size=len(adj))
    docs = []
    for r in adj.itertuples(index=False):
        docs.append({
            "movement_id": int(r.movement_id), "product_id": int(r.product_id), "warehouse_id": int(r.warehouse_id),
            "action": "STOCK_ADJUSTMENT", "quantity_change": int(r.quantity),
            "previous_quantity": int(r.previous_quantity), "new_quantity": int(r.new_quantity),
            "reason": r.reason, "reason_category": CATEGORY.get(r.reason, "OTHER"),
            "performed_by": r.performed_by, "timestamp": r.movement_date.to_pydatetime(),
            "details": {"reference_no": r.reference_no, "source": "mysql.stock_movements"},
        })
    return docs


def main():
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=5000)
    logs = client[os.getenv("MONGO_DB", "inventory_audit")]["stock_audit_logs_loaded"]
    logs.drop()
    docs = build_documents()
    logs.insert_many(docs)
    logs.create_index([("product_id", ASCENDING)], name="idx_product")
    logs.create_index([("warehouse_id", ASCENDING)], name="idx_warehouse")
    logs.create_index([("product_id", ASCENDING), ("warehouse_id", ASCENDING), ("timestamp", DESCENDING)],
                      name="idx_product_wh_time")
    logs.create_index([("movement_id", ASCENDING)], name="uq_movement", unique=True)
    print(f"Inserted {len(docs):,} audit documents into {logs.full_name}")
    print("Indexes:", [i["name"] for i in logs.list_indexes()])
    print("Example:", logs.find_one({"product_id": docs[0]["product_id"]}, {"_id": 0}))


if __name__ == "__main__":
    main()
