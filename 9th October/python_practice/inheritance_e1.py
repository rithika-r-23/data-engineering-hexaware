class Employee:
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary
    def display_employee(self):
        print("Name:",self.name)
        print("Salary:",self.salary)
class Developer(Employee):
    pass


d1=Developer("Rithika",200000)
d1.display_employee()

