sales = [
    ("North", 12000),
    ("South", 18000),
    ("West", 9500),
    ("North", 22000),
    ("East", 15000),
    ("South", 11000)
]

regions = set(item[0] for item in sales)

print(regions)