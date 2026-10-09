class Employee:
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary

    def display_employee(self):
        print("Name:",self.name)
        print("Salary:",self.salary)
class Developer(Employee):
    def write_code(self):
        print("Dev is writing code")

d1=Developer("Sara",5000)
d1.display_employee()
d1.write_code()