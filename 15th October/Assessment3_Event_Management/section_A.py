

# Q1
attendee_name = input()
tickets = int(input())
ticket_price = float(input())

# Q2
total_amount = tickets * ticket_price

# Q3
if total_amount >= 10000:
    discount = total_amount * 0.10
else:
    discount = total_amount * 0.05

final_amount = total_amount - discount

# Q4
print(f"Attendee Name: {attendee_name}")
print(f"Tickets: {tickets}")
print(f"Ticket Price: Rs. {ticket_price:.2f}")
print(f"Total Amount: Rs. {total_amount:.2f}")
print(f"Discount: Rs. {discount:.2f}")
print(f"Final Amount: Rs. {final_amount:.2f}")

# Q5
capacity = int(input())
registered = int(input())

# Q6
if registered == capacity:
    print("Full")
elif registered < capacity:
    print(f"Seats Available ({capacity - registered} seats left)")
else:
    print("Invalid Data")

# Q7
for number in range(1, 16):
    print(number, end=" ")
print()

# Q8
for number in range(1, 16):
    if number % 3 == 0:
        print(number, end=" ")
print()

# Q9
count = 10
while count >= 1:
    print(count, end=" ")
    count -= 1
print()

# Q10
for number in range(1, 11):
    if number == 7:
        continue
    print(number, end=" ")
print()

seat_capacity = 5
for seat in range(1, 11):
    if seat > seat_capacity:
        break
    print(f"Registration {seat} accepted")