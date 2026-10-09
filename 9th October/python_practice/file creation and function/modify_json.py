import json
with open("products.json", "r") as f:
    products = json.load(f)

for p in products:
    if p["product_id"]==101:
        p["price"]=70000

with open("products.json", "w") as f:
    json.dump(products, f,indent=4)