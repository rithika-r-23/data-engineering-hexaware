# Q11-25

booking_amounts = [
    5000, 3500, 7500, 6000,
    4000, 7000, 3000, 10000
]

# Q11
total_amount = sum(booking_amounts)
print(total_amount)

# Q12
average_amount = total_amount / len(booking_amounts)
print(f"{average_amount:.2f}")

# Q13
print(max(booking_amounts))
print(min(booking_amounts))

# Q14
print([a for a in booking_amounts if a > 5000])

# Q15
print(sorted(booking_amounts, reverse=True))

cities = [
    "Hyderabad",
    "Mumbai",
    "Pune",
    "Hyderabad",
    "Delhi",
    "Mumbai"
]

# Q16
unique_cities = set(cities)
print(unique_cities)

# Q17
unique_cities.add("Chennai")
print(unique_cities)

# Q18
print(len(unique_cities))

# Q19
event = ("E101", "AI Innovation Summit", "Hyderabad", 500)
print(event)

# Q20
event_id, event_name, venue, capacity = event
print(event_id)
print(event_name)
print(venue)
print(capacity)

# Q21
registration = {
    "registration_id": "R1001",
    "attendee_name": "Aarav Shah",
    "city": "Hyderabad",
    "tickets": 2,
    "status": "Confirmed",
    "amount": 5000
}
print(registration)

# Q22
registration["status"] = "Cancelled"
print(registration["status"])

# Q23
registration["tickets"] += 1
print(registration["tickets"])

# Q24
registration["email"] = "aarav.shah@example.com"
print(registration["email"])

# Q25
for key, value in registration.items():
    print(f"{key}: {value}")