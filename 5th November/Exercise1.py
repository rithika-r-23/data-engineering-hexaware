# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE courier_parcels_delta (
# MAGIC parcel_id INT,
# MAGIC customer_name STRING,
# MAGIC destination_city STRING,
# MAGIC service_type STRING,
# MAGIC weight_kg DOUBLE,
# MAGIC shipping_fee INT,
# MAGIC delivery_status STRING
# MAGIC )
# MAGIC USING DELTA;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO courier_parcels_delta VALUES
# MAGIC (101, 'Arjun', 'Hyderabad', 'Express', 2.5, 500, 'Delivered'),
# MAGIC (102, 'Meera', 'Mumbai', 'Standard', 4.0, 350, 'In Transit'),
# MAGIC (103, 'Karan', 'Delhi', 'Express', 1.5, 450, 'Pending'),
# MAGIC (104, 'Sneha', 'Pune', 'Standard', 3.0, 300, 'Delivered'),
# MAGIC (105, 'Rohit', 'Chennai', 'Express', 5.0, 800, 'In Transit'),
# MAGIC (106, 'Divya', 'Hyderabad', 'Standard', 2.0, 250, 'Cancelled'),
# MAGIC (107, 'Nikhil', 'Bengaluru', 'Express', 6.0, 950, 'Delivered'),
# MAGIC (108, 'Pooja', 'Mumbai', 'Standard', 1.0, 150, 'Pending'),
# MAGIC
# MAGIC (109, 'Vikram', 'Delhi', 'Express', 3.5, 650, 'In Transit'),
# MAGIC (110, 'Anjali', 'Pune', 'Standard', 4.5, 400, 'Cancelled'),
# MAGIC (111, 'Farhan', 'Chennai', 'Express', 2.0, 550, 'Delivered'),
# MAGIC (112, 'Kavya', 'Hyderabad', 'Standard', 5.5, 600, 'Pending'),
# MAGIC (113, 'Manoj', 'Bengaluru', 'Express', 1.5, 400, 'In Transit'),
# MAGIC (114, 'Riya', 'Delhi', 'Standard', 3.0, 300, 'Delivered'),
# MAGIC (115, 'Tarun', 'Mumbai', 'Express', 4.0, 700, 'Pending');

# COMMAND ----------

# MAGIC %md
# MAGIC Part A — Creating Delta tables

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE courier_parcels_copy
# MAGIC USING DELTA
# MAGIC AS SELECT * FROM courier_parcels_delta;

# COMMAND ----------

data = [
    (201, "Aman", "Kochi", "Express", 2.0, 500, "Pending"),
    (202, "Latha", "Nagpur", "Standard", 3.5, 320, "In Transit"),
    (203, "Zoya", "Lucknow", "Express", 1.0, 420, "Delivered")
]
schema = "parcel_id INT, customer_name STRING, destination_city STRING, service_type STRING, weight_kg DOUBLE, shipping_fee INT, delivery_status STRING"
pyspark_df = spark.createDataFrame(data, schema)
pyspark_df.write.format("delta").mode("overwrite").saveAsTable("courier_parcels_pyspark")
display(spark.table("courier_parcels_pyspark"))

# COMMAND ----------

tables = ["courier_parcels_delta", "courier_parcels_copy", "courier_parcels_pyspark"]
for t in tables:
    display(spark.sql(f"DESCRIBE DETAIL {t}").select("name", "format", "location"))

# COMMAND ----------

# MAGIC %md
# MAGIC Part B: INSERT, UPDATE and DELETE

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO courier_parcels_delta
# MAGIC VALUES (116, 'Sameer', 'Jaipur', 'Express', 2.5, 550, 'Pending');
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta
# MAGIC SET delivery_status = 'Delivered'
# MAGIC WHERE parcel_id = 103;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta
# MAGIC SET shipping_fee = shipping_fee + 100
# MAGIC WHERE service_type = 'Express';

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta
# MAGIC SET destination_city = 'Hyderabad'
# MAGIC WHERE parcel_id = 108;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM courier_parcels_delta
# MAGIC WHERE delivery_status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta
# MAGIC ORDER BY shipping_fee DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Part C: MERGE and UPSERT

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW incoming_parcels AS
# MAGIC SELECT *
# MAGIC FROM VALUES
# MAGIC (102, 'Meera', 'Mumbai', 'Express', 4.0, 650, 'Delivered'),
# MAGIC (105, 'Rohit', 'Chennai', 'Express', 5.0, 900, 'Delivered'),
# MAGIC (117, 'Ayesha', 'Kolkata', 'Standard', 2.0, 300, 'Pending'),
# MAGIC (118, 'Rahul', 'Jaipur', 'Express', 3.0, 600, 'In Transit')
# MAGIC AS incoming(
# MAGIC parcel_id,
# MAGIC customer_name,
# MAGIC destination_city,
# MAGIC service_type,
# MAGIC weight_kg,
# MAGIC shipping_fee,
# MAGIC delivery_status
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM incoming_parcels;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.parcel_id
# MAGIC FROM incoming_parcels i
# MAGIC INNER JOIN courier_parcels_delta t ON i.parcel_id = t.parcel_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.parcel_id
# MAGIC FROM incoming_parcels i
# MAGIC LEFT ANTI JOIN courier_parcels_delta t ON i.parcel_id = t.parcel_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO courier_parcels_delta AS t
# MAGIC USING incoming_parcels AS s
# MAGIC ON t.parcel_id = s.parcel_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta
# MAGIC WHERE parcel_id IN (102, 105);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta
# MAGIC WHERE parcel_id IN (117, 118);

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Part D: Delta table internals and Time Travel
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL courier_parcels_delta;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY courier_parcels_delta;

# COMMAND ----------

history_df = spark.sql("DESCRIBE HISTORY courier_parcels_delta")
merge_version = history_df.filter("operation = 'MERGE'").agg({"version": "max"}).collect()[0][0]
print(merge_version - 1)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta VERSION AS OF 6
# MAGIC ORDER BY parcel_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'previous' AS version_label, *
# MAGIC FROM courier_parcels_delta VERSION AS OF 6
# MAGIC WHERE parcel_id = 102
# MAGIC UNION ALL
# MAGIC SELECT 'current' AS version_label, *
# MAGIC FROM courier_parcels_delta
# MAGIC WHERE parcel_id = 102;

# COMMAND ----------

# MAGIC %md
# MAGIC Part E: OPTIMIZE

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE courier_parcels_delta ZORDER BY (destination_city);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY courier_parcels_delta;