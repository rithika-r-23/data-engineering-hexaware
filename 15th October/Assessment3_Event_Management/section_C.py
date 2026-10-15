

# Q26
def calculate_booking(ticket_price, tickets):
    return ticket_price * tickets

print(calculate_booking(2500, 2))


# Q27
def calculate_discount(amount):
    if amount >= 10000:
        return amount * 0.10
    return amount * 0.05

print(calculate_discount(10000))
print(calculate_discount(5000))


# Q28
def is_active(status):
    return status in ("Confirmed", "Pending")

print(is_active("Confirmed"))
print(is_active("Pending"))
print(is_active("Cancelled"))


# Q29
def total_bookings(amounts):
    return sum(amounts)

booking_amounts = [5000, 3500, 7500, 6000, 4000, 7000, 3000, 10000]
print(total_bookings(booking_amounts))


# Q30
increase_10 = lambda amount: amount * 1.10
print(increase_10(5000))


# Q31
above_6000 = list(filter(lambda a: a > 6000, booking_amounts))
print(above_6000)


# Q32
registrations = [
    {"registration_id": "R1001", "attendee_name": "Aarav Shah", "city": "Hyderabad", "tickets": 2, "status": "Confirmed", "amount": 5000},
    {"registration_id": "R1002", "attendee_name": "Simran Kaur", "city": "Mumbai", "tickets": 1, "status": "Confirmed", "amount": 3500},
    {"registration_id": "R1003", "attendee_name": "Faiz Ahmed", "city": "Pune", "tickets": 3, "status": "Pending", "amount": 7500},
    {"registration_id": "R1004", "attendee_name": "Keerthi Rao", "city": "Bangalore", "tickets": 2, "status": "Confirmed", "amount": 6000},
    {"registration_id": "R1005", "attendee_name": "Mohit Kapoor", "city": "Delhi", "tickets": 1, "status": "Cancelled", "amount": 4000},
    {"registration_id": "R1006", "attendee_name": "Ananya Das", "city": "Hyderabad", "tickets": 2, "status": "Confirmed", "amount": 7000},
    {"registration_id": "R1007", "attendee_name": "Zubin Patel", "city": "Mumbai", "tickets": 1, "status": "Pending", "amount": 3000},
    {"registration_id": "R1008", "attendee_name": "Sonal Mehta", "city": "Delhi", "tickets": 4, "status": "Confirmed", "amount": 10000}
]

confirmed = list(filter(lambda r: r["status"] == "Confirmed", registrations))
for r in confirmed:
    print(f"{r['registration_id']}  {r['attendee_name']}  {r['city']}  {r['amount']}")


# Q33
cities = list(map(lambda r: r["city"], registrations))
print(cities)


# Q34
unique_cities = set(map(lambda r: r["city"], registrations))
print(unique_cities)


# Q35
sorted_by_amount = sorted(registrations, key=lambda r: r["amount"])
for r in sorted_by_amount:
    print(f"{r['registration_id']}  {r['attendee_name']}  {r['amount']}")