import pandas as pd
df=pd.read_csv("orders.csv")

res=(
    df.groupby("status")
    .size()

)
print(res)