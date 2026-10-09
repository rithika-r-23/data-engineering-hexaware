products=["Laptop","Mouse","Keyboard","Monitor"]
print(products)
print(products[0])
print(products[1])
print(products[-1])

products[1]="Wireless mouse"
print(products)
products.append("Disk")
print(products)

products.insert(1,"Led monitor")
print(products)

products.remove("Laptop")
print(products)

products.pop()

