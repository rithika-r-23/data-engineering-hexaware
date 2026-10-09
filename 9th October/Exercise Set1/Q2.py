import csv
with open("shipments.csv") as file:
    reader=csv.DictReader(file)
    shipments=list(reader)
print(shipments)
