import json

with open("projects.json", "r") as file:
    projects = json.load(file)

total_members = 0

for project in projects:
    total_members += len(project["team"])

print("Total team members:", total_members)