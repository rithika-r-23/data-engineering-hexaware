import csv

with open("shipments.csv", "r") as file:
    shipments = list(csv.DictReader(file))

cities = list(map(lambda s: s["city"], shipments))
print(cities)