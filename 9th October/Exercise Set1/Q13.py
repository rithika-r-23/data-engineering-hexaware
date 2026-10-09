import csv

with open("shipments.csv", "r") as file:
    shipments = list(csv.DictReader(file))

sorted_shipments = sorted(
    shipments, key=lambda s: float(s["weight"]), reverse=True
)

for s in sorted_shipments:
    print(s["shipment_id"],s["weight"])