import csv

with open("shipments.csv", "r", newline="") as file:
    shipments = list(csv.DictReader(file))

total = sum(float(s["cost"]) for s in shipments)
print("Total shipping cost:", total)