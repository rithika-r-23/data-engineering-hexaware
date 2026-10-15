# Q18-20
class Shipment:
    # Q19
    def __init__(self, shipment_id, destination, weight, cost):
        self.shipment_id = shipment_id
        self.destination = destination
        self.weight = weight
        self.cost = cost

    # Q20
    def display(self):
        print(f"ID: {self.shipment_id}, Destination: {self.destination}, "
              f"Weight: {self.weight} kg, Cost: {self.cost}")

    def calculate_total_cost(self):
        return self.cost


# Q21
class ExpressShipment(Shipment):
    def __init__(self, shipment_id, destination, weight, cost, express_surcharge):
        super().__init__(shipment_id, destination, weight, cost)
        self.express_surcharge = express_surcharge

    # Q22
    def calculate_total_cost(self):
        return self.cost + self.express_surcharge

    def display(self):
        print(f"ID: {self.shipment_id}, Destination: {self.destination}, "
              f"Weight: {self.weight} kg, Cost: {self.cost}, "
              f"Surcharge: {self.express_surcharge}")


normal_shipment = Shipment("S1001", "Hyderabad", 12.5, 850)
express_shipment = ExpressShipment("S1003", "Bangalore", 18.5, 1250, 300)

normal_shipment.display()
print(normal_shipment.calculate_total_cost())

express_shipment.display()
print(express_shipment.calculate_total_cost())


# Q23
shipment_objects = [
    Shipment("S1001", "Hyderabad", 12.5, 850),
    ExpressShipment("S1003", "Bangalore", 18.5, 1250, 300),
    Shipment("S1005", "Pune", 22.0, 1600),
    ExpressShipment("S1010", "Pune", 25.0, 1750, 400),
]

for obj in shipment_objects:
    obj.display()
    print(obj.calculate_total_cost())