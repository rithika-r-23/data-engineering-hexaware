shipments = [
    {"shipment_id": "S1001", "destination": "Hyderabad", "weight": 12.5, "status": "Delivered", "cost": 850},
    {"shipment_id": "S1002", "destination": "Mumbai", "weight": 8.0, "status": "In Transit", "cost": 620},
    {"shipment_id": "S1003", "destination": "Bangalore", "weight": 18.5, "status": "Delivered", "cost": 1250},
    {"shipment_id": "S1004", "destination": "Delhi", "weight": 5.5, "status": "Pending", "cost": 480},
    {"shipment_id": "S1005", "destination": "Pune", "weight": 22.0, "status": "Delivered", "cost": 1600},
    {"shipment_id": "S1006", "destination": "Hyderabad", "weight": 10.0, "status": "In Transit", "cost": 740},
]


# Q13
def calculate_shipping_cost(weight, rate_per_kg=70):
    return weight * rate_per_kg

print(calculate_shipping_cost(12.5))
print(calculate_shipping_cost(10, 80))


# Q14
def get_shipment_category(weight):
    if weight > 20:
        return "Heavy"
    elif weight >= 10:
        return "Medium"
    return "Light"

for s in shipments:
    print(f"{s['shipment_id']}  {s['weight']} kg  {get_shipment_category(s['weight'])}")


# Q15
delivered = list(filter(lambda s: s["status"] == "Delivered", shipments))
for s in delivered:
    print(f"{s['shipment_id']}  {s['destination']}  {s['status']}")


# Q16
all_destinations = list(map(lambda s: s["destination"], shipments))
print(all_destinations)


# Q17
sorted_by_cost = sorted(shipments, key=lambda s: s["cost"])
for s in sorted_by_cost:
    print(f"{s['shipment_id']}  {s['destination']}  {s['cost']}")