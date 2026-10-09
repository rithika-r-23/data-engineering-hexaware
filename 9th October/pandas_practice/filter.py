import pandas as pd

df=pd.read_csv("orders.csv")


delivered=df.query("status=='Delivered'")
print(delivered)

result=df.query("amount > 20000")
print(result)

