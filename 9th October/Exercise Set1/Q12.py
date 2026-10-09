import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

sorted_shipments = sorted(shipments, key=lambda s: float(s["cost"]))



for s in sorted_shipments:
    print(s["shipment_id"], s["cost"])