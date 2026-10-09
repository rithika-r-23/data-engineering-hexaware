import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

for s in shipments:
    print(s["shipment_id"], s["customer"], s["status"])