#key-value pair
product={
    "product_id":101,
    "product_name":"Laptop",
    "category":"Electronics",
    "price":65000
}


print(product)
#Acess
print(product["product_id"])

#get without error
print(product.get("price"))

product["price"]=70000
print(product)
#add a new key value pair
product["stock"]=20
print(product)

#remove
product.pop("category")
del product["price"]




