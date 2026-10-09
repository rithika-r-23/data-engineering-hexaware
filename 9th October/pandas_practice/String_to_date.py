import pandas as pd
df=pd.read_csv("orders.csv")

df["order_date"]= pd.to_datetime(df["order_date"])
df["month"]=df["order_date"].dt.month

print(df)