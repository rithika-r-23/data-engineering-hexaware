import csv
with open("shipments.csv","r") as file:
    shipments=list(csv.DictReader(file))

for s in shipments:
    if float(s["cost"]) > 700:
        print(s)
