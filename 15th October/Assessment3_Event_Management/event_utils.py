
#Q75
def calculate_booking_amount(ticket_price, tickets):
    return ticket_price * tickets


#Q75
def calculate_discount(amount):
    if amount >= 10000:
        return amount * 0.10
    return amount * 0.05


#Q75
def check_event_capacity(capacity, registered):
    if registered == capacity:
        return "Full"
    elif registered < capacity:
        return "Seats Available"
    return "Invalid Data"