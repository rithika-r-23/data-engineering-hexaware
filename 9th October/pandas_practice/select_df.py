import pandas as pd

df=pd.read_csv("orders.csv")
print(df["product"])
print(df[["order_id","product","amount"]])
