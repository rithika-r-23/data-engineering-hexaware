import csv

with open("shipments.csv", "r") as file:
    shipments = list(csv.DictReader(file))

heavy = list(filter(lambda s: float(s["weight"]) > 10, shipments))
print(heavy)