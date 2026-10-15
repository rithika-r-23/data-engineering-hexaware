

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

customers_df = pd.read_csv(os.path.join(BASE_DIR, "customers.csv"))
orders_df = pd.read_csv(os.path.join(BASE_DIR, "orders.csv"))

orders_df["order_value"] = orders_df["quantity"] * orders_df["unit_price"]

merged = pd.merge(orders_df, customers_df, on="customer_id", how="inner")
# Q82
merged["order_size"] = np.select(
    [merged["order_value"] >= 50000, merged["order_value"] >= 15000],
    ["High", "Medium"],
    default="Low"
)
print(merged[["order_id", "order_value", "order_size"]])

# Q83
merged["priority_customer"] = np.where(
    merged["segment"] == "Corporate", "Priority", "Normal"
)
print(merged[["order_id", "customer_name", "segment", "priority_customer"]])

# Q84
merged.to_csv(os.path.join(BASE_DIR, "orders_updated.csv"), index=False)