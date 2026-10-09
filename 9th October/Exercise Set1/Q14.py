import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

sorted_shipments = sorted(shipments, key=lambda s: s["customer"])

for s in sorted_shipments:
    print(s["customer"])