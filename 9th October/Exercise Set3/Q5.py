import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    if "Python" in project["technologies"]:
        print(project["project_name"])