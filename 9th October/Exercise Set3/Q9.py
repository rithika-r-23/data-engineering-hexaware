import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    print("\nProject:", project["project_name"])

    for member in project["team"]:
        print("Name:", member["name"])
        print("Role:", member["role"])
        print("Experience:", member["experience"])