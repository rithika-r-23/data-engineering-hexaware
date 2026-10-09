import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

for s in shipments:
    s["weight"] = float(s["weight"])
    s["cost"] = float(s["cost"])

print(shipments)