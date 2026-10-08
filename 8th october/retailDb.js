
use("retail_db")

db.products_schema_demo.insertMany([
    {
        product_id: 101,
        product_name: "Laptop",
        category: "Electronics",
        price: 65000,
        stock: 10
    },
    {
        product_id: 102,
        name: "Wireless Mouse",
        category: "Electronics",
        price: "1500",
        stock: 25
    },
    {
        product_id: 103,
        product_name: "Office Chair",
        category: "Furniture",
        price: 8500,
        quantity: 12
    },
    {
        product_id: 104,
        product_name: "Keyboard",
        category: 100,
        price: 2500,
        stock: "20"
    }
])

db.products_structure.insertOne({
    product_id: 201,
    product_name: "Gaming Laptop",
    brand: "Lenovo",
    category: "Electronics",
    price: 85000,
    ram: "16 GB",
    storage: "1 TB SSD",
    processor: "Intel Core i7"
})

db.products_structure.insertOne({
    product_id: 202,
    product_name: "Gaming Laptop",
    brand: "Lenovo",
    category: "Electronics",
    price: 85000,

    specifications: {
        ram: "16 GB",
        storage: "1 TB SSD",
        processor: "Intel Core i7"
    }
})

db.products_structure.insertOne({
    product_id: 203,
    product_name: "Office Desk",
    category: "Furniture",
    price: 12000,

    supplier: {
        supplier_name: "Home Furnishings",
        city: "Hyderabad",
        phone: "9876543210"
    }
})

db.products_structure.insertOne({
    product_id: 204,
    product_name: "Running Shoes",
    category: "Footwear",
    price: 4500,

    colors: [
        "Black",
        "White",
        "Blue"
    ]
})

db.products_structure.find({
    colors: "Black"
})

db.products_structure.insertOne({
    product_id: 205,
    product_name: "Smart Watch",
    category: "Electronics",
    price: 15000,

    reviews: [
        {
            customer: "Rohan",
            rating: 5,
            comment: "Excellent"
        },
        {
            customer: "Meera",
            rating: 4,
            comment: "Good battery"
        },
        {
            customer: "Kabir",
            rating: 3,
            comment: "Average display"
        }
    ]
})

db.createCollection("datatype_demo")

db.datatype_demo.insertOne({
    product_id: 301,

    product_name: "Smart TV",              // String

    price: 45999.99,                       // Double

    stock: NumberInt(25),                  // Integer

    total_views: NumberLong(150000),        // Long

    available: true,                       // Boolean

    launch_date: ISODate("2026-10-01"),    // Date

    discount: null,                        // Null

    tags: [
        "Electronics",
        "Smart TV",
        "4K"
    ],                                     // Array

    specifications: {
        screen_size: "55 inch",
        resolution: "4K",
        wifi: true
    },                                     // Embedded Document

    product_code: ObjectId()               // ObjectId
})

db.datatype_practice.insertMany([
{
product_id: 501,
product_name: "Laptop",
price: 65000,
stock: 10,
available: true,
launch_date: ISODate("2026-01-10"),
colors: ["Black", "Silver"],
details: {
brand: "Dell",
warranty_years: 2
}
},
{
product_id: 502,
product_name: "Headphones",
price: 4500,
stock: 25,
available: true,
launch_date: ISODate("2026-03-15"),
colors: ["Black", "Blue"],
details: {
brand: "Sony",
warranty_years: 1
}
},
{
product_id: 503,
product_name: "Office Chair",
price: 9000,
stock: 0,
available: false,
launch_date: ISODate("2025-12-20"),

colors: ["Black", "Grey"],
details: {
brand: "GreenSoul",
warranty_years: 3
}
},
{
product_id: 504,
product_name: "Smart Watch",
price: 18000,
stock: 8,
available: true,
launch_date: ISODate("2026-06-01"),
colors: ["Black", "Red"],
details: {
brand: "Samsung",
warranty_years: 1
}
}
])

//Practice Questions

db.datatype_practice.find()

db.datatype_practice.find({})

db.datatype_practice.find({product_name: "Laptop"})

db.datatype_practice.find({price:{$gt:10000}})

db.datatype_practice.find({stock:{$lt:10}})

db.datatype_practice.find({available:false})

db.datatype_practice.find({launch_date:{$gt :ISODate("2026-01-01")}})

db.datatype_practice.find({colors:"Black"})

db.datatype_practice.find({colors:{$all: ["Black","Blue"]}})

db.datatype_practice.find({"details.brand":"Samsung"})

db.datatype_practice.find({"details.warranty_years":{$gt:1}})

db.datatype_practice.updateOne({product_id:502},{$inc:{stock:5}})

db.datatype_practice.updateOne({product_id:503},{$set:{available:true}})

db.datatype_practice.updateOne({product_id:501},{$set:{colors:"white"}})

db.datatype_practice.updateOne({product_id:504},{$set:{"details.warranty_years":2}})

db.datatype_practice.find({},{_id:0,product_name:1,price:1})

db.datatype_practice.aggregate([{$project:{product_name:1,price_type:{$type:"$price"}}}])

db.datatype_practice.aggregate([{$project:{product_name:1,available_type:{$type:"$available"}}}])

db.datatype_practice.aggregate([{$project:{product_name:1,launch_date_type:{$type:"$launch_date"}}}])

db.datatype_practice.aggregate([{$project:{product_name:1,colors_type:{$type:"$colors"}}}])
