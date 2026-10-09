
import json

with open("projects.json", "r") as file:
    projects = json.load(file)

print(type(projects))