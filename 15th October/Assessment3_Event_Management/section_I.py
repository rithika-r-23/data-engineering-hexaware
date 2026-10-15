import os
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q80
df = pd.read_csv(os.path.join(BASE_DIR, "registrations.csv"))
print("Registrations loaded into a DataFrame")

# Q81
print(df.head())
print(df.tail())
print("Shape:", df.shape)
print("Columns:", list(df.columns))
print(df.dtypes)

# Q82
print(df[["attendee_name", "city", "status", "amount"]])

# Q83
print(df.query('status == "Confirmed"'))

# Q84
print(df[df["amount"] > 6000])

# Q85
print(df.query('status == "Confirmed" and city == "Hyderabad"'))

# Q86
print(df["status"].value_counts())

# Q87
print(df.groupby("status")["amount"].sum())

# Q88
print(df.groupby("city")["amount"].mean().round(2))