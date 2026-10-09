import json

with open("projects.json", "r") as file:
    projects = json.load(file)

technologies = []

for project in projects:
    technologies.extend(project["technologies"])

unique_technologies = set(technologies)

print(unique_technologies)