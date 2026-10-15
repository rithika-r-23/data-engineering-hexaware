import os

# Q47-52
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(BASE_DIR, "event_log.txt")

# Q47
with open(log_path, "w") as file:
    file.write("Event E101 registration processing started\n")
    file.write("Event E102 registration processing started\n")
    file.write("Event E103 registration processing started\n")

# Q48
with open(log_path, "a") as file:
    file.write("Event E104 registration processing started\n")
    file.write("All event registrations processed successfully\n")

# Q49
with open(log_path, "r") as file:
    content = file.read()
print(content)

# Q50-51
with open(log_path, "r") as file:
    for line_number, line in enumerate(file, start=1):
        print(f"{line_number}. {line.strip()}")