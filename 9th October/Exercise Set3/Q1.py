import json

with open("projects.json", "r") as file:
    projects = json.load(file)

print(projects)