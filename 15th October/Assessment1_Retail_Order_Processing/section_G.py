import pandas as pd
import os

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q61
orders_path = os.path.join(BASE_DIR, "orders.csv")
df = pd.read_csv(orders_path)

# Q62
print(df.head())

# Q63
print(df.dtypes)

# Q64
print(df.shape)

# Q65
delivered = df.query('stat == "Delivered"')
print(delivered)

# Q66
print(df[df["quantity"] > 2])

# Q67
df["order_value"] = df["quantity"] * df["unit_price"]
print(df[["order_id", "quantity", "unit_price", "order_value"]])

# Q68
print(df["stat"].value_counts())

# Q69
df["order_date"] = pd.to_datetime(df["order_date"])
print(df["order_date"].dtype)

# Q70
df["month"] = df["order_date"].dt.to_period("M").astype(str)
print(df[["order_id", "order_date", "month"]])

# Q71
print(df.groupby(["month", "stat"]).size().reset_index(name="order_count"))

# Q72
print(df.groupby("category")["order_value"].sum())

# Q73
print(df.groupby("category")["order_value"].mean().round(2))

# Q74
print(df.sort_values("order_value", ascending=False))