# Q30
class Product:
    def __init__(self, product_id, product_name, price, stock):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.stock = stock

    # Q31
    def display_product(self):
        print(f"ID: {self.product_id}  Name: {self.product_name}  "
              f"Price: {self.price}  Stock: {self.stock}")

    # Q32
    def calculate_value(self):
        return self.price * self.stock


# Q33
laptop = Product(201, "Laptop", 65000, 12)
monitor = Product(202, "Monitor", 18000, 8)

laptop.display_product()
monitor.display_product()
print(f"Laptop stock value: {laptop.calculate_value()}")
print(f"Monitor stock value: {monitor.calculate_value()}")


# Q34-Q37
class DiscountedProduct(Product):
    def __init__(self, product_id, product_name, price, stock, discount_percent):
        super().__init__(product_id, product_name, price, stock)
        self.discount_percent = discount_percent

    def display_product(self):
        discounted_price = self.price - (self.price * self.discount_percent / 100)
        print(f"ID: {self.product_id}  Name: {self.product_name}  "
              f"Price: {self.price}  Stock: {self.stock}  "
              f"Discount: {self.discount_percent}%  "
              f"Price after discount: {discounted_price:.2f}")


# Q38
class PremiumProduct(Product):
    def __init__(self, product_id, product_name, price, stock, warranty_years):
        super().__init__(product_id, product_name, price, stock)
        self.warranty_years = warranty_years

    def display_product(self):
        print(f"ID: {self.product_id}  Name: {self.product_name}  "
              f"Price: {self.price}  Stock: {self.stock}  "
              f"Warranty: {self.warranty_years} years  Premium Quality")


# Q39
products_list = [
    Product(204, "Keyboard", 3000, 30),
    DiscountedProduct(203, "Office Chair", 9000, 15, 10),
    PremiumProduct(201, "Laptop Pro", 120000, 5, 3),
]

for item in products_list:
    item.display_product()