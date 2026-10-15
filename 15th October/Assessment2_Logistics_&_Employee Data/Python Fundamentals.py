# Q1
weight = float(input())
cost = float(input())

# Q2
cost_per_kg = cost / weight
print(f"Weight: {weight} kg")
print(f"Cost: Rs. {cost:,.2f}")
print(f"Cost per kg: Rs. {cost_per_kg:,.2f}")

# Q3
if weight > 20:
    category = "Heavy"
elif weight >= 10:
    category = "Medium"
else:
    category = "Light"

print(f"Classification: {category}")

# Q4
for number in range(1, 21):
    print(number, end=" ")
print()

# Q5
for number in range(1, 21):
    if number % 2 == 0:
        print(number, end=" ")
print()

# Q6
attempt = 1
while attempt <= 5:
    print(f"Processing attempt {attempt} of 5")
    attempt += 1

print("All five attempts completed")