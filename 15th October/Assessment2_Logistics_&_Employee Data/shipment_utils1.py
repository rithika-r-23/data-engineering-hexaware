def calculate_shipping_cost(weight, rate_per_kg=70):
    return weight * rate_per_kg


def calculate_cost_per_kg(cost, weight):
    return cost / weight


def get_shipment_category(weight):
    if weight > 20:
        return "Heavy"
    elif weight >= 10:
        return "Medium"
    return "Light"