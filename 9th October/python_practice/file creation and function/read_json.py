import json
with open("products.json","r") as file:
    products=json.load(file)

for p in products:
    print(p)
    