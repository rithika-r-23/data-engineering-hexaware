#q1
product_name = input("Enter product name:")
unit_price = float(input("Enter unit price:"))
quantity = int(input("Enter quantity:"))
#q2
total_amount = unit_price * quantity
#q3
if total_amount >= 50000:
    discount = total_amount * 0.10
else:
    discount = total_amount * 0.05
final_amount = total_amount - discount

#q4
print(f"\nProduct         : {product_name}")
print(f"Original Amount : Rs. {total_amount:,.2f}")
print(f"Discount        : Rs. {discount:,.2f}")
print(f"Final Amount    : Rs. {final_amount:,.2f}")

#Q5
stock = int(input("\nEnter stock quantity: "))
if stock > 20:
    print("High Stock")
elif 1 <= stock <= 20:
    print("Low Stock")
elif stock == 0:
    print("Out of Stock")
else:
    print("Invalid stock quantity")

#Q6
print("\nQ6. Numbers 1 to 10:")
for i in range(1, 11):
    print(i, end=" ")
print()

#Q7
print("\nQ7. Reducing stock from 5 to 0:")
stock_level = 5
while stock_level >= 0:
    print(f"Stock: {stock_level}")
    stock_level -= 1

#q8
print("\nQ8. Numbers 1 to 10 (skipping 5):")
for i in range(1, 11):
    if i == 5:
        continue
    print(i, end=" ")
print()

#Q9
print("\nQ9. Numbers 1 to 10 (stop at 8):")
for i in range(1, 11):
    if i == 8:
        break
    print(i, end=" ")
print()
