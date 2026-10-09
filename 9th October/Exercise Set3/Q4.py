import json

with open("projects.json", "r") as file:
    projects = json.load(file)

for project in projects:
    if project["budget"] > 400000:
        print(project["project_name"], project["budget"])