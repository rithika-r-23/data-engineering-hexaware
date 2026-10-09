import csv


with open("shipments.csv","r") as file:
    shipments=list(csv.DictReader(file))

deliver=list(filter(lambda s: s["status"] =="Delivery", shipments))
print(deliver)