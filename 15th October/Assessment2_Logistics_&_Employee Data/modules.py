# Q34
import shipment_utils1

print(shipment_utils1.calculate_shipping_cost(12.5))
print(shipment_utils1.get_shipment_category(22))


# Q35
from shipment_utils1 import calculate_cost_per_kg

print(f"{calculate_cost_per_kg(1600, 22):.2f}")