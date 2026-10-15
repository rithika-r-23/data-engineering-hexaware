
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q36
shipments_df = pd.read_csv(os.path.join(BASE_DIR, "shipments.csv"))
print(shipments_df.shape)
print(shipments_df)


# Q37
print(shipments_df[shipments_df["status"] == "Delivered"])


# Q38
print(shipments_df["status"].value_counts())


# Q39
shipments_df["shipment_date"] = pd.to_datetime(shipments_df["shipment_date"])
print(shipments_df["shipment_date"].dtype)


# Q40
shipments_df["month"] = shipments_df["shipment_date"].dt.to_period("M").astype(str)
print(shipments_df.groupby(["month", "status"]).size().reset_index(name="shipment_count"))


# Q41
print(shipments_df.groupby("destination")["cost"].mean().round(2))


# Q42
print(shipments_df.groupby("destination")["weight"].sum())


# Q43
csv_path = os.path.join(BASE_DIR, "shipments.csv")
wanted_columns = ["shipment_id", "destination", "weight", "cost", "status"]
available_columns = pd.read_csv(csv_path, nrows=0).columns
selected_columns = [c for c in wanted_columns if c in available_columns]
selected_df = pd.read_csv(csv_path, usecols=selected_columns)
print(selected_df.head())


# Q44
hubs_df = pd.read_csv(os.path.join(BASE_DIR, "hubs.csv"))
print(hubs_df)


# Q45
merged = pd.merge(shipments_df, hubs_df, on="hub_id", how="inner")
print(merged.shape)
print(merged[["shipment_id", "hub_id", "hub_name", "destination", "status", "cost"]])


# Q46-47
hub_summary = merged.groupby(["hub_id", "hub_name"]).agg(
    total_shipment_cost=("cost", "sum"),
    total_shipments=("shipment_id", "count")
).reset_index()

print(hub_summary)


# Q48
hub_summary = hub_summary.sort_values(
    "total_shipment_cost", ascending=False
).reset_index(drop=True)

print(hub_summary)


# Q49
hub_summary.to_csv(os.path.join(BASE_DIR, "hub_summary.csv"), index=False)


# Q50
hub_summary.to_json(
    os.path.join(BASE_DIR, "hub_summary.json"),
    orient="records",
    indent=4
)