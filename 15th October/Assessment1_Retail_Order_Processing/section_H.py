import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q75
customers_df = pd.read_csv(os.path.join(BASE_DIR, "customers.csv"))
orders_df = pd.read_csv(os.path.join(BASE_DIR, "orders.csv"))
orders_df["order_value"] = orders_df["quantity"] * orders_df["unit_price"]

merged = pd.merge(orders_df, customers_df, on="customer_id", how="inner")
print(merged.shape)

# Q76
print(merged[["order_id", "customer_name", "city", "product", "stat", "order_value"]])

# Q77
hyd_delivered = merged.query('stat == "Delivered" and city == "Hyderabad"')
print(hyd_delivered[["order_id", "customer_name", "city", "product", "stat", "order_value"]])

# Q78
city_summary = merged.groupby("city").agg(
    total_orders=("order_id", "count"),
    total_sales=("order_value", "sum"),
    average_order_value=("order_value", "mean")
).reset_index()

city_summary["average_order_value"] = city_summary["average_order_value"].round(2)
print(city_summary)

# Q79
city_summary = city_summary.sort_values("total_sales", ascending=False).reset_index(drop=True)
print(city_summary)

# Q80
city_summary.to_csv(os.path.join(BASE_DIR, "city_sales.csv"), index=False)

# Q81
city_summary.to_json(
    os.path.join(BASE_DIR, "city_sales.json"),
    orient="records",
    indent=4
)