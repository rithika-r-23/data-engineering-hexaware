
sales = [65000, 4500, 36000, 12000, 18000, 72000, 9000]# Q21
def calculate_total(price, quantity):
    return price * quantity

print("calculate_total(1500, 3) =", calculate_total(1500, 3))

# Q22
def calculate_discount(amount):
    if amount >= 50000:
        return amount * 0.10
    return amount * 0.05

print("calculate_discount(65000) =", calculate_discount(65000))
print("calculate_discount(4500) =", calculate_discount(4500))

# Q23
def total_sales(sales_list):
    return sum(sales_list)

print("total_sales(sales) =", total_sales(sales))

# Q24
def check_availability(product_dict):
    if product_dict.get("stock", 0) > 0:
        return "Available"
    return "Out of Stock"

print(check_availability({"product_name": "Laptop", "stock": 12}))
print(check_availability({"product_name": "Monitor", "stock": 0}))

# Q25
square = lambda n: n * n
print("square(7) =", square(7))

# Q26
high_sales = list(filter(lambda s: s > 20000, sales))
print("Sales > 20000:", high_sales)

# Q27
customers = [
    {"customer_id": "C101", "customer_name": "North Star Retail", "city": "Hyderabad"},
    {"customer_id": "C102", "customer_name": "Blue Mart", "city": "Mumbai"},
    {"customer_id": "C104", "customer_name": "Prime Stores", "city": "Hyderabad"},
    {"customer_id": "C105", "customer_name": "Fresh Point", "city": "Delhi"},
    {"customer_id": "C106", "customer_name": "Quick Buy", "city": "Pune"},
]
customer_cities = list(map(lambda c: c["city"], customers))
print("Customer cities:", customer_cities)

# Q28
print("Unique cities:", set(customer_cities))

# Q29
products = [
    {"product_id": 201, "product_name": "Laptop", "price": 65000},
    {"product_id": 202, "product_name": "Monitor", "price": 18000},
    {"product_id": 203, "product_name": "Office Chair", "price": 9000},
    {"product_id": 204, "product_name": "Keyboard", "price": 3000},
]
sorted_products = sorted(products, key=lambda p: p["price"])
print("Products sorted by price (low to high):")
for p in sorted_products:
    print(f"{p['product_name']}: {p['price']}")