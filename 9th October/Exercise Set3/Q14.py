import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    sorted_team = sorted(
        project["team"],
        key=lambda member: member["experience"]
    )

    print("\nProject:", project["project_name"])

    for member in sorted_team:
        print(member["name"], member["experience"])