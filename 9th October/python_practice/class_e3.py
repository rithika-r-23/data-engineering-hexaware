class Product:
    name=""
    price=0

    def display(self):
        print(f"Product name: {self.name}")
        print(f"Product price: {self.price}")



p1=Product()
p1.name="Mouse"
p1.price=1000
p1.display()
