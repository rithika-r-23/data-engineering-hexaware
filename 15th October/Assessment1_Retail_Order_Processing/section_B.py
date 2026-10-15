sales = [65000, 4500, 36000, 12000, 18000, 72000, 9000]

# Q10
print(f"Total sales: {sum(sales)}")

# Q11
print(f"Highest sale: {max(sales)}")
print(f"Lowest sale : {min(sales)}")

# Q12
print("Sales > 20000:", [s for s in sales if s > 20000])

# Q13
print("Sorted (high to low):", sorted(sales, reverse=True))

# Q14
cities = ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Pune", "Mumbai"]
unique_cities = set(cities)
print("Unique cities:", unique_cities)

# Q15
product = (201, "Laptop", "Electronics", 65000)
product_id, p_name, p_category, p_price = product
print("Unpacked tuple:")
print(f"ID={product_id}, Name={p_name}, Category={p_category}, Price={p_price}")

# Q16
customer = {
    "id": "C101",
    "name": "North Star Retail",
    "city": "Hyderabad",
    "orders": 3,
    "active": True,
}
print("Customer:", customer)

# Q17
customer["city"] = "Chennai"
print("After city update:", customer["city"])

# Q18
customer["orders"] += 1
print("Orders after increase:", customer["orders"])

# Q19
customer["email"] = "contact@northstar.com"
print("Email added:", customer["email"])

# Q20
print("Customer details:")
for key, value in customer.items():
    print(f"{key}: {value}")