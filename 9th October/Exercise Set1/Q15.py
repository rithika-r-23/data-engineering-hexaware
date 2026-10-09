import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

cost_per_kg = lambda s: float(s["cost"]) / float(s["weight"])

for s in shipments:
    print(s["shipment_id"], round(cost_per_kg(s), 2))