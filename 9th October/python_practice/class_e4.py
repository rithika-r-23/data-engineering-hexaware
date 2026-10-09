class Product:
    name=""
    price=0
    quantity=0

    def total_amount(self):
        return self.price*self.quantity

p1=Product()
p1.name="Mouse"
p1.price=1000
p1.quantity=5
print(p1.name,p1.price,p1.quantity)
print(f"Total amount: {p1.total_amount()}")