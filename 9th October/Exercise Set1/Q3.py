import csv
with open("shipments.csv","r") as file:
    shipments = list(csv.DictReader(file))

print(shipments)