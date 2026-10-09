import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    print(project["project_name"])