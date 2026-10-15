import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "registrations.csv")

# Q53,Q54
registrations = []
with open(csv_path, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        registrations.append(row)
print(f"Read {len(registrations)} records into a list")

# Q55
for r in registrations:
    if r["status"] == "Confirmed":
        print(f"{r['registration_id']}, {r['attendee_name']}, {r['city']}, {r['amount']}")

# Q56
for r in registrations:
    if r["city"] == "Hyderabad":
        print(f"{r['registration_id']}, {r['attendee_name']}, {r['status']}, {r['amount']}")

# Q57
for r in registrations:
    r["amount"] = int(r["amount"])
print("Amount converted to int. Type of first amount:", type(registrations[0]["amount"]).__name__)

# Q58
for r in registrations:
    if r["amount"] > 7000:
        print(f"{r['registration_id']}, {r['attendee_name']}, {r['amount']}")

# Q59
total_amount = sum(r["amount"] for r in registrations)
print(f"Total registration amount: {total_amount}")

# Q60
all_cities = [r["city"] for r in registrations]
print("All cities:", all_cities)
print("Unique cities:", sorted(set(all_cities)))