import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    for member in project["team"]:
        if member["experience"] > 3:
            print(member["name"], member["experience"])