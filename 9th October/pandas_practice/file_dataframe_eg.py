import pandas as pd

df = pd.read_csv("orders.csv")

print(df.head())
print(df.tail())

print(df.columns)
print(df.shape)

df.info()