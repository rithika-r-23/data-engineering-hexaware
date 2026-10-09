class Employee:
    def work(self):
        print("Emp is working")

class Developer(Employee):
    def code(self):
        print("Developer is writing Python code")

class Tester(Employee):
    def test(self):
        print("Testing application")

d1=Developer()
d1.work()
d1.code()
print("Next")
t1=Tester()
t1.work()
t1.test()