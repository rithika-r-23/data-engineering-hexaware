import retail_utils

# Q58
order_total = retail_utils.calculate_order_total(65000, 2)
order_discount = retail_utils.calculate_discount(order_total)
stock_status = retail_utils.check_stock(12)

print(f"Order total: {order_total}")
print(f"Discount: {order_discount}")
print(f"Stock status: {stock_status}")

# Q59
from retail_utils import check_stock

print(f"check_stock(0): {check_stock(0)}")
print(f"check_stock(30): {check_stock(30)}")

# Q60
import retail_utils as ru

print(f"ru.calculate_order_total(1500, 3): {ru.calculate_order_total(1500, 3)}")
print(f"ru.calculate_discount(4500): {ru.calculate_discount(4500)}")
print(f"ru.check_stock(5): {ru.check_stock(5)}")