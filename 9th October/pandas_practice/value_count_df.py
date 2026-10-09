import pandas as pd
df=pd.read_csv("orders.csv")
print(
    df["status"].value_counts()
)