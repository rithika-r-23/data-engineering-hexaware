# Q76
import event_utils

# Q77
amount = event_utils.calculate_booking_amount(2500, 4)
discount = event_utils.calculate_discount(amount)
capacity_status = event_utils.check_event_capacity(500, 500)

print("Booking amount:", amount)
print("Discount:", discount)
print("Capacity status:", capacity_status)

# Q78
from event_utils import check_event_capacity

print("Capacity status:", check_event_capacity(500, 350))
print("Capacity status:", check_event_capacity(500, 520))

# Q79
import event_utils as eu

print("Booking amount:", eu.calculate_booking_amount(3500, 2))
print("Discount:", eu.calculate_discount(7000))
print("Capacity status:", eu.check_event_capacity(300, 120))