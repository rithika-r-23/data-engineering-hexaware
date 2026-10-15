import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q51-54
shipments_df = pd.read_csv(os.path.join(BASE_DIR, "shipments.csv"))
hubs_df = pd.read_csv(os.path.join(BASE_DIR, "hubs.csv"))
df = pd.merge(shipments_df, hubs_df, on="hub_id", how="inner")


# Q51
df["cost_per_kg"] = (df["cost"] / df["weight"]).round(2)
print(df[["shipment_id", "weight", "cost", "cost_per_kg"]])


# Q52
df["cost_class"] = np.where(df["cost"] >= 1200, "Expensive", "Normal")
print(df[["shipment_id", "cost", "cost_class"]])


# Q53
conditions = [
    (df["status"] == "Delivered") & (df["cost"] >= 1200),
    (df["status"] == "Delivered"),
    (df["status"] == "In Transit") & (df["cost"] >= 1200),
    (df["status"] == "In Transit"),
    (df["status"] == "Pending") & (df["cost"] >= 1200)
]

categories = [
    "Completed - High Value",
    "Completed - Standard",
    "Monitor - High Value",
    "On Track",
    "Delay Risk - High Value"
]

df["performance_category"] = np.select(
    conditions, categories, default="Pending - Standard"
)

print(df[["shipment_id", "status", "cost", "performance_category"]])
print(df["performance_category"].value_counts())


# Q54
output_path = os.path.join(BASE_DIR, "shipment_results.csv")
df.to_csv(output_path, index=False)