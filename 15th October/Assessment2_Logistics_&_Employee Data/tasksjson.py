import tasksjson
import os

# Q24
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "employees.json"), "r") as f:
    employees = tasksjson.load(f)
print(len(employees))


# Q25
print([e["name"] for e in employees])


# Q26
for e in employees:
    if e["salary"] > 75000:
        print(f"{e['name']} - {e['salary']}")


# Q27
for e in employees:
    if "Python" in e["skills"]:
        print(f"{e['name']} - {e['skills']}")


# Q28
for e in employees:
    print(f"{e['name']}: {e['performance']['rating']}")


# Q29
for e in employees:
    if e["performance"]["rating"] > 4.5:
        print(f"{e['name']} - {e['performance']['rating']}")


# Q30
sorted_employees = sorted(
    employees,
    key=lambda e: e["performance"]["rating"],
    reverse=True
)

for e in sorted_employees:
    print(f"{e['name']}: {e['performance']['rating']}")


# Q31
for e in employees:
    if e["employee_id"] == 303:
        print(e["skills"])
        e["skills"].append("Python")
        print(e["skills"])


# Q32
updated_path = os.path.join(BASE_DIR, "employees_updated.json")

with open(updated_path, "w") as f:
    tasksjson.dump(employees, f, indent=4)