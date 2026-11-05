# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE cafe_orders_demo (
# MAGIC     order_id INT,
# MAGIC     customer_name STRING,
# MAGIC     city STRING,
# MAGIC     amount INT,
# MAGIC     order_status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO cafe_orders_demo VALUES
# MAGIC (101, 'Ayaan', 'Hyderabad', 450, 'Completed'),
# MAGIC (102, 'Tara', 'Mumbai', 700, 'Pending'),
# MAGIC (103, 'Ishaan', 'Pune', 300, 'Completed'),
# MAGIC (104, 'Sara', 'Hyderabad', 900, 'Completed'),
# MAGIC (105, 'Kabir', 'Delhi', 250, 'Cancelled'),
# MAGIC (106, 'Zoya', 'Mumbai', 600, 'Pending'),
# MAGIC (107, 'Rehan', 'Pune', 800, 'Completed'),
# MAGIC (108, 'Mira', 'Delhi', 550, 'Completed');

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED cafe_orders_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS

# COMMAND ----------

# MAGIC %sql
# MAGIC USE SCHEMA DEFAULT;
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE rithika_databricks.default.bike_rides_raw (
# MAGIC     ride_id INT,
# MAGIC     station STRING,
# MAGIC     duration_min INT,
# MAGIC     fare DOUBLE,
# MAGIC     status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO rithika_databricks.default.bike_rides_raw VALUES
# MAGIC (1, 'Central', 20, 100.0, 'Completed'),
# MAGIC (2, 'Airport', 35, 180.0, 'Completed'),
# MAGIC (3, 'Metro', 15, 75.0, 'Cancelled'),
# MAGIC (4, 'Central', 40, 200.0, 'Completed'),
# MAGIC (5, 'University', 25, 125.0, 'Completed');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM rithika_databricks.default.bike_rides_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_bronze_sql
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM STREAM(rithika_databricks.default.bike_rides_raw);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_bronze_sql
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM STREAM(rithika_databricks.default.bike_rides_raw);
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_silver_sql
# MAGIC AS
# MAGIC SELECT
# MAGIC     ride_id,
# MAGIC     station,
# MAGIC     duration_min,
# MAGIC     fare
# MAGIC FROM STREAM(bike_bronze_sql)
# MAGIC WHERE status = 'Completed'
# MAGIC   AND duration_min > 0
# MAGIC   AND fare > 0;

# COMMAND ----------

import matplotlib.pyplot as plt
df = spark.sql("""
    SELECT station, total_rides, total_revenue
    FROM rithika_databricks.default.bike_gold_sql
""")
pdf = df.toPandas()
plt.figure(figsize=(10, 5))
plt.bar(pdf["station"], pdf["total_revenue"])
plt.xlabel("Station")
plt.ylabel("Total Revenue (₹)")

# COMMAND ----------

import matplotlib.pyplot as plt

df = spark.sql("""
    SELECT station, total_rides, total_revenue
    FROM rithika_databricks.default.bike_gold_sql
""")

pdf = df.toPandas()



# COMMAND ----------

plt.figure(figsize=(7, 7))

plt.pie(
    pdf["total_revenue"],
    labels=pdf["station"],
    autopct="%1.1f%%",
    startangle=90
)

# COMMAND ----------

pdf = pdf.sort_values("station")

plt.figure(figsize=(10, 5))

plt.plot(
    pdf["station"],
    pdf["total_revenue"],
    marker="o"
)

plt.xlabel("Station")
plt.ylabel("Total Revenue (₹)")
plt.title("Revenue by Station")
plt.grid(True)
plt.show()  

# COMMAND ----------

plt.figure(figsize=(10, 5))

plt.scatter(
    pdf["total_rides"],
    pdf["total_revenue"],
    s=100
)

for _, row in pdf.iterrows():
    plt.annotate(
        row["station"],
        (row["total_rides"], row["total_revenue"]),
        xytext=(5, 5),
        textcoords="offset points"
    )

plt.xlabel("Total Rides")
plt.ylabel("Total Revenue (₹)")
plt.title("Total Rides vs Revenue")
plt.grid(True)
plt.show()