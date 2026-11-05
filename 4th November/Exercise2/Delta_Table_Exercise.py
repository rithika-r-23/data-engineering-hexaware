# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE fitness_memberships_demo (
# MAGIC member_id INT,
# MAGIC member_name STRING,
# MAGIC city STRING,
# MAGIC membership_plan STRING,
# MAGIC monthly_fee INT,
# MAGIC duration_months INT,
# MAGIC status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO fitness_memberships_demo VALUES
# MAGIC (101, 'Arjun', 'Hyderabad', 'Premium', 3000, 12, 'Active'),
# MAGIC (102, 'Sneha', 'Pune', 'Basic', 1000, 3, 'Active'),
# MAGIC (103, 'Kiran', 'Chennai', 'Standard', 2000, 6, 'Expired'),
# MAGIC (104, 'Meera', 'Hyderabad', 'Basic', 1000, 6, 'Active'),
# MAGIC (105, 'Vikram', 'Delhi', 'Premium', 3000, 12, 'Active'),
# MAGIC (106, 'Anjali', 'Pune', 'Standard', 2000, 3, 'Cancelled'),
# MAGIC (107, 'Rohit', 'Mumbai', 'Basic', 1000, 3, 'Active'),
# MAGIC (108, 'Divya', 'Chennai', 'Premium', 3000, 6, 'Expired'),
# MAGIC (109, 'Sanjay', 'Hyderabad', 'Standard', 2000, 12, 'Active'),
# MAGIC (110, 'Pooja', 'Delhi', 'Basic', 1000, 3, 'Cancelled'),
# MAGIC (111, 'Nikhil', 'Mumbai', 'Premium', 3000, 12, 'Active'),
# MAGIC
# MAGIC (112, 'Kavya', 'Pune', 'Standard', 2000, 6, 'Active'),
# MAGIC (113, 'Manoj', 'Chennai', 'Basic', 1000, 3, 'Expired'),
# MAGIC (114, 'Riya', 'Hyderabad', 'Premium', 3000, 12, 'Active'),
# MAGIC (115, 'Deepak', 'Delhi', 'Standard', 2000, 6, 'Active'),
# MAGIC (116, 'Neha', 'Mumbai', 'Basic', 1000, 3, 'Cancelled'),
# MAGIC (117, 'Tarun', 'Pune', 'Premium', 3000, 12, 'Active'),
# MAGIC (118, 'Aisha', 'Chennai', 'Standard', 2000, 6, 'Active'),
# MAGIC (119, 'Harish', 'Hyderabad', 'Basic', 1000, 3, 'Expired'),
# MAGIC (120, 'Simran', 'Delhi', 'Premium', 3000, 12, 'Active');

# COMMAND ----------

# MAGIC %md
# MAGIC Part A: Retrieving and filtering data

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT member_name, city, membership_plan
# MAGIC FROM fitness_memberships_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE city = 'Hyderabad';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE monthly_fee > 2000;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT city FROM fitness_memberships_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE membership_plan IN ('Premium', 'Standard');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE monthly_fee BETWEEN 1000 AND 2000;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE member_name LIKE 'S%';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE status = 'Active' AND city = 'Hyderabad';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo
# MAGIC WHERE city = 'Pune' OR city = 'Chennai';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT member_name AS Name, monthly_fee AS Fee
# MAGIC FROM fitness_memberships_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT m.*
# MAGIC FROM fitness_memberships_demo AS m
# MAGIC WHERE m.membership_plan = 'Premium';

# COMMAND ----------

# MAGIC %md
# MAGIC Part B: Modifying Delta table records

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO fitness_memberships_demo
# MAGIC VALUES (121, 'Farhan', 'Jaipur', 'Premium', 3000, 6, 'Active');

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE fitness_memberships_demo
# MAGIC SET monthly_fee = 1500
# MAGIC WHERE member_name = 'Sneha';

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE fitness_memberships_demo
# MAGIC SET status = 'Active'
# MAGIC WHERE member_name = 'Kiran' AND status = 'Expired';

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE fitness_memberships_demo
# MAGIC SET monthly_fee = monthly_fee + 500
# MAGIC WHERE membership_plan = 'Premium';

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM fitness_memberships_demo
# MAGIC WHERE status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM fitness_memberships_demo
# MAGIC WHERE member_id = 113;

# COMMAND ----------

# MAGIC %md
# MAGIC Part C: Delta table operations

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY fitness_memberships_demo;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fitness_memberships_demo VERSION AS OF 2;

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH old_v AS (
# MAGIC   SELECT * FROM fitness_memberships_demo VERSION AS OF 2
# MAGIC ),
# MAGIC cur AS (
# MAGIC   SELECT * FROM fitness_memberships_demo
# MAGIC )
# MAGIC SELECT
# MAGIC   COALESCE(old_v.member_id, cur.member_id) AS member_id,
# MAGIC   COALESCE(old_v.member_name, cur.member_name) AS member_name,
# MAGIC   old_v.monthly_fee AS old_fee,
# MAGIC   cur.monthly_fee AS current_fee,
# MAGIC   old_v.status AS old_status,
# MAGIC   cur.status AS current_status
# MAGIC FROM old_v
# MAGIC FULL OUTER JOIN cur ON old_v.member_id = cur.member_id
# MAGIC WHERE NOT (old_v.monthly_fee <=> cur.monthly_fee AND old_v.status <=> cur.status)
# MAGIC ORDER BY member_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS remaining_records
# MAGIC FROM fitness_memberships_demo;