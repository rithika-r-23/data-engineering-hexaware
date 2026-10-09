class Employee:
    def __init__(self,emp_id,name,department,salary):
        self.emp_id=emp_id
        self.name=name
        self.department=department
        self.salary=salary
e1=Employee(101,"Arun","IT",65000)
e2=Employee(102,"Sara","IT",50000)

print(e1.name,e1.salary)
print(e2.name,e2.salary)