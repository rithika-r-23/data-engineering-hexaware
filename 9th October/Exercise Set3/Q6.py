import json

with open("projects.json", "r") as file:
    projects = json.load(file)

total_budget = sum(project["budget"] for project in projects)

print("Total budget:", total_budget)