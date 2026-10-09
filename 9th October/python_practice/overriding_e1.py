from inheritance_e1 import d1


class  Employee:
    def work(self):
        print("Emp is working")
class Developer(Employee):
    def work(self):
        print("Developer is writing code")

e1=Employee()
d1=Developer()

e1.work()
d1.work()
