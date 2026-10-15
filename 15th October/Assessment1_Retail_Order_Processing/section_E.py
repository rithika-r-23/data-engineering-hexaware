
import csv
import tasksjson
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q40 & Q41
activity_path = os.path.join(BASE_DIR, "activity.txt")
with open(activity_path, "w") as f:
    f.write("Order 1001 processing started\n")
    f.write("Order 1002 processing started\n")
    f.write("Order 1003 processing started\n")

# Q42
with open(activity_path, "a") as f:
    f.write("Order 1004 processing completed\n")

# Q43
with open(activity_path, "r") as f:
    print(f.read())

# Q44 & Q45
customers_path = os.path.join(BASE_DIR, "customers.csv")
customer_records = []
with open(customers_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        customer_records.append(row)

# Q46
for c in customer_records:
    if c["active"] == "True":
        print(f"{c['customer_id']}  {c['customer_name']}  {c['city']}  {c['segment']}")

# Q47
for c in customer_records:
    if c["city"] == "Hyderabad":
        print(f"{c['customer_id']}  {c['customer_name']}  {c['segment']}")

# Q48
products_path = os.path.join(BASE_DIR, "products.json")
with open(products_path, "r") as f:
    product_data = tasksjson.load(f)

# Q49
print([p["product_name"] for p in product_data])

# Q50
for p in product_data:
    if p["price"] > 10000:
        print(f"{p['product_name']}  {p['price']}")

# Q51
for p in product_data:
    print(f"{p['product_name']}: {p['supplier']['name']}  {p['supplier']['city']}")

# Q52
all_colors = []
for p in product_data:
    all_colors.extend(p["colors"])
print(all_colors)

# Q53
print(set(all_colors))

# Q54
for p in product_data:
    if p["product_id"] == 202:
        print(f"Stock before: {p['stock']}")
        p["stock"] += 10
        print(f"Stock after: {p['stock']}")

# Q55
updated_path = os.path.join(BASE_DIR, "products_updated.json")
with open(updated_path, "w") as f:
    tasksjson.dump(product_data, f, indent=4)