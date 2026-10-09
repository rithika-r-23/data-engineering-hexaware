import json

with open("projects.json", "r") as file:
    projects = json.load(file)

sorted_projects = sorted(
    projects,
    key=lambda project: project["budget"],
    reverse=True
)

for project in sorted_projects:
    print(project["project_name"], project["budget"])