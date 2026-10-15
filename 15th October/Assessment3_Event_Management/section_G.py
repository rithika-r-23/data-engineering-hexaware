import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Q61
with open(os.path.join(BASE_DIR, "staff.json"), "r") as file:
    staff = json.load(file)
print(f"Read {len(staff)} staff records from staff.json")

# Q62
print("Type of returned object:", type(staff).__name__)
print("Type of each item:", type(staff[0]).__name__)

# Q63
print("Staff names:", [s["name"] for s in staff])

# Q64
for s in staff:
    if s["department"] == "Operations":
        print(f"{s['name']}, {s['department']}")

# Q65
for s in staff:
    if s["salary"] > 75000:
        print(f"{s['name']}, {s['salary']}")

# Q66
for s in staff:
    if "Python" in s["skills"]:
        print(f"{s['name']}, {s['skills']}")

# Q67
for s in staff:
    print(f"{s['name']}, {s['performance']['rating']}, {s['performance']['events_handled']}")

# Q68
for s in staff:
    if s["performance"]["rating"] > 4.5:
        print(f"{s['name']}, {s['performance']['rating']}")

# Q69
all_skills = []
for s in staff:
    all_skills.extend(s["skills"])
print("All skills:", all_skills)

# Q70
print("Unique skills:", sorted(set(all_skills)))

# Q71
for s in sorted(staff, key=lambda s: s["salary"], reverse=True):
    print(f"{s['name']}, {s['salary']}")

# Q72
for s in sorted(staff, key=lambda s: s["performance"]["rating"], reverse=True):
    print(f"{s['name']}, {s['performance']['rating']}")

# Q73
for s in staff:
    if s["staff_id"] == 503:
        print("Skills before:", s["skills"])
        s["skills"].append("Pandas")
        print("Skills after:", s["skills"])

# Q74
with open(os.path.join(BASE_DIR, "staff_updated.json"), "w") as file:
    json.dump(staff, file, indent=4)
print("Modified data saved to staff_updated.json")
