# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE office_inventory_demo (
# MAGIC     product_id INT,
# MAGIC     product_name STRING,
# MAGIC     category STRING,
# MAGIC     city STRING,
# MAGIC     price INT,
# MAGIC     quantity INT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO office_inventory_demo VALUES
# MAGIC (101, 'Laptop', 'Electronics', 'Hyderabad', 55000, 10),
# MAGIC (102, 'Mouse', 'Accessories', 'Bengaluru', 800, 50),
# MAGIC (103, 'Keyboard', 'Accessories', 'Mumbai', 1500, 30),
# MAGIC (104, 'Monitor', 'Electronics', 'Hyderabad', 12000, 15),
# MAGIC (105, 'Office Chair', 'Furniture', 'Delhi', 6500, 20),
# MAGIC (106, 'Desk', 'Furniture', 'Chennai', 9000, 12),
# MAGIC (107, 'Printer', 'Electronics', 'Mumbai', 18000, 8),
# MAGIC (108, 'Webcam', 'Accessories', 'Hyderabad', 2500, 25),
# MAGIC (109, 'Projector', 'Electronics', 'Delhi', 45000, 5),
# MAGIC (110, 'Headphones', 'Accessories', 'Bengaluru', 3000, 40);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM office_inventory_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE office_inventory_demo
# MAGIC SET price = 60000
# MAGIC WHERE product_id = 101;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE office_inventory_demo
# MAGIC SET price = 1000,
# MAGIC     quantity = 60
# MAGIC WHERE product_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE office_inventory_demo
# MAGIC SET price = 1000,
# MAGIC     quantity = 60
# MAGIC WHERE product_id = 102;

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC SELECT product_name, price
# MAGIC FROM office_inventory_demo;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM office_inventory_demo
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM office_inventory_demo