cities={"Hydrabad","Mumbai","Delhi","Hydrabad"}
print(cities)

cities.add("Pune")
print(cities)

cities.remove("Mumbai")
print(cities)

cities.discard("Chennai")
print(cities)

#typecast
cities=[
    "Hydrabad",
    "Mumbai",
    "Delhi",
    "Hydrabad",
    "Mumbai",
]
unique_cities=set(cities)
print(unique_cities)