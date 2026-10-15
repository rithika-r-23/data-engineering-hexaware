
class Event:
    # Q36
    def __init__(self, event_id, event_name, capacity, ticket_price):
        self.event_id = event_id
        self.event_name = event_name
        self.capacity = capacity
        self.ticket_price = ticket_price

    # Q37
    def display_event(self):
        print(f"ID: {self.event_id}, Name: {self.event_name}, "
              f"Capacity: {self.capacity}, Ticket Price: {self.ticket_price}")

    # Q38
    def calculate_revenue(self, tickets_sold):
        return tickets_sold * self.ticket_price


# Q39
event1 = Event("E101", "AI Innovation Summit", 500, 2500)
event2 = Event("E102", "Leadership Forum", 350, 3500)

event1.display_event()
print(event1.calculate_revenue(100))

event2.display_event()
print(event2.calculate_revenue(50))


# Q40-42
class OnlineEvent(Event):
    def __init__(self, event_id, event_name, capacity, ticket_price, platform):
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.platform = platform

    # Q42
    def display_event(self):
        print(f"ID: {self.event_id}, Name: {self.event_name}, "
              f"Capacity: {self.capacity}, Ticket Price: {self.ticket_price}, "
              f"Platform: {self.platform}")


# Q43-44
class PhysicalEvent(Event):
    def __init__(self, event_id, event_name, capacity, ticket_price, venue):
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.venue = venue

    # Q44
    def display_event(self):
        print(f"ID: {self.event_id}, Name: {self.event_name}, "
              f"Capacity: {self.capacity}, Ticket Price: {self.ticket_price}, "
              f"Venue: {self.venue}")


# Q45
events = [
    OnlineEvent("E201", "Data Engineering Webinar", 1000, 500, "Zoom"),
    PhysicalEvent("E103", "Data Engineering Bootcamp", 200, 3000, "Bangalore"),
    OnlineEvent("E202", "Cloud Skills Live", 800, 750, "Microsoft Teams"),
    PhysicalEvent("E104", "Startup Connect", 300, 2000, "Delhi")
]

# Q46
for event in events:
    event.display_event()