# Q7
shipment_costs = [850, 620, 1250, 480, 1600, 740, 590, 1100, 920, 1750, 520, 1050]
print(shipment_costs)

# Q8
total_cost = sum(shipment_costs)
average_cost = total_cost / len(shipment_costs)
print(f"Total: {total_cost}")
print(f"Average: {average_cost:.2f}")
print(f"Minimum: {min(shipment_costs)}")
print(f"Maximum: {max(shipment_costs)}")

# Q9
destinations = [
    "Hyderabad", "Mumbai", "Bangalore", "Delhi", "Pune", "Hyderabad",
    "Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Mumbai",
]
unique_destinations = set(destinations)
print(unique_destinations)

# Q10
shipment = {
    "shipment_id": "S1001",
    "hub_id": "H01",
    "shipment_date": "2026-06-01",
    "destination": "Hyderabad",
    "weight": 12.5,
    "status": "Delivered",
    "cost": 850,
}
print(shipment)

# Q11
shipments = [
    {"shipment_id": "S1001", "hub_id": "H01", "shipment_date": "2026-06-01", "destination": "Hyderabad", "weight": 12.5, "status": "Delivered", "cost": 850},
    {"shipment_id": "S1002", "hub_id": "H02", "shipment_date": "2026-06-03", "destination": "Mumbai", "weight": 8.0, "status": "In Transit", "cost": 620},
    {"shipment_id": "S1003", "hub_id": "H01", "shipment_date": "2026-06-06", "destination": "Bangalore", "weight": 18.5, "status": "Delivered", "cost": 1250},
    {"shipment_id": "S1004", "hub_id": "H03", "shipment_date": "2026-06-10", "destination": "Delhi", "weight": 5.5, "status": "Pending", "cost": 480},
    {"shipment_id": "S1005", "hub_id": "H02", "shipment_date": "2026-07-02", "destination": "Pune", "weight": 22.0, "status": "Delivered", "cost": 1600},
    {"shipment_id": "S1006", "hub_id": "H03", "shipment_date": "2026-07-06", "destination": "Hyderabad", "weight": 10.0, "status": "In Transit", "cost": 740},
]

for s in shipments:
    print(f"{s['shipment_id']}  {s['destination']}  {s['weight']} kg  {s['status']}  {s['cost']}")

# Q12
delivered_shipments = [s for s in shipments if s["status"] == "Delivered"]
for s in delivered_shipments:
    print(f"{s['shipment_id']}  {s['destination']}  {s['cost']}")

in_transit_shipments = [s for s in shipments if s["status"] == "In Transit"]
for s in in_transit_shipments:
    print(f"{s['shipment_id']}  {s['destination']}  {s['cost']}")