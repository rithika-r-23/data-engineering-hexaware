import json

with open("projects.json", "r") as file:
    projects = json.load(file)

sorted_projects = sorted(
    projects,
    key=lambda project: project["project_name"]
)

for project in sorted_projects:
    print(project["project_name"])