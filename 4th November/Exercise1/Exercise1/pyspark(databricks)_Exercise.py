# Databricks notebook source


# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

csv_path = "/Workspace/Users/azuser7412_mml.local@karthikirisoutlook.onmicrosoft.com/pyspark_exercise1/cinema_bookings.csv"
json_path = "/Workspace/Users/azuser7412_mml.local@karthikirisoutlook.onmicrosoft.com/pyspark_exercise1/cinema_master.json"



# COMMAND ----------

# MAGIC %md
# MAGIC A.Read and inspect the data
# MAGIC

# COMMAND ----------

bookings_df = spark.read.csv(csv_path, header=True, inferSchema=True)

# COMMAND ----------

cinemas_df = spark.read.json(json_path)
display(bookings_df)
display(cinemas_df)

# COMMAND ----------

bookings_df.printSchema()
cinemas_df.printSchema()
print([(f.name, f.dataType.simpleString()) for f in cinemas_df.schema.fields])

# COMMAND ----------

display(bookings_df.limit(10))
print(bookings_df.count())

# COMMAND ----------

display(bookings_df.select("booking_id", "movie_title", "tickets", "booking_status"))

# COMMAND ----------

# MAGIC %md
# MAGIC B. Filter, clean and transform

# COMMAND ----------

display(bookings_df.filter(F.col("booking_status") == "Confirmed"))

# COMMAND ----------

display(bookings_df.filter(F.col("booking_status") == "Confirmed"))

# COMMAND ----------

display(bookings_df.filter((F.col("tickets") > 3) & (F.col("price_per_ticket") > 200)))

# COMMAND ----------

display(
    bookings_df.select(
        [F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in ["discount_pct", "payment_method"]]
    )
)

# COMMAND ----------

cleaned_df = bookings_df.fillna({"discount_pct": 0, "payment_method": "Unknown"})
display(cleaned_df)

# COMMAND ----------

cleaned_df = cleaned_df.withColumn("gross_amount", F.col("tickets") * F.col("price_per_ticket"))
display(cleaned_df)

# COMMAND ----------

cleaned_df = cleaned_df.withColumn(
    "net_amount",
    F.round(F.col("gross_amount") * (1 - F.col("discount_pct") / 100), 2).cast("double")
)
display(cleaned_df)

# COMMAND ----------

cleaned_df = cleaned_df.withColumn(
    "booking_size",
    F.when(F.col("tickets") >= 4, "Large").otherwise("Regular")
)
display(cleaned_df)

# COMMAND ----------

display(cleaned_df.orderBy(F.col("net_amount").desc()).limit(5))


# COMMAND ----------

# MAGIC %md
# MAGIC C. Aggregations and joins

# COMMAND ----------

display(cleaned_df.groupBy("booking_status").count())


# COMMAND ----------

display(
    cleaned_df.filter(F.col("booking_status") == "Confirmed")
    .groupBy("movie_title")
    .agg(
        F.sum("tickets").alias("total_tickets"),
        F.round(F.sum("net_amount"), 2).alias("net_revenue")
    )
    .orderBy(F.col("net_revenue").desc())
)

# COMMAND ----------

display(
    cleaned_df.filter(F.col("booking_status") == "Confirmed")
    .groupBy("cinema_id")
    .agg(F.round(F.sum("net_amount"), 2).alias("net_revenue"))
    .orderBy(F.col("net_revenue").desc())
    .limit(3)
)

# COMMAND ----------

joined_df = cleaned_df.join(cinemas_df, on="cinema_id", how="left")
display(joined_df)

# COMMAND ----------

display(
    joined_df.select(
        "cinema_name",
        F.col("location.city").alias("city"),
        "movie_title",
        "booking_status"
    )
)

# COMMAND ----------

display(
    joined_df.filter(F.col("booking_status") == "Confirmed")
    .groupBy(F.col("location.city").alias("city"))
    .agg(F.round(F.sum("net_amount"), 2).alias("net_revenue"))
    .orderBy(F.col("net_revenue").desc())
)
display(joined_df.filter(F.col("cinema_name").isNull()))

# COMMAND ----------

# MAGIC %md
# MAGIC D. JSON, dates and DataFrame quality

# COMMAND ----------

display(
    cinemas_df.select("cinema_id", "cinema_name", F.explode("facilities").alias("facility"))
)

# COMMAND ----------

dated_df = (
    cleaned_df
    .withColumn("booking_date", F.to_date(F.col("booking_date")))
    .withColumn("show_date", F.to_date(F.col("show_date")))
    .withColumn("days_between_booking_and_show", F.datediff(F.col("show_date"), F.col("booking_date")))
)
display(dated_df.select("booking_id", "booking_date", "show_date", "days_between_booking_and_show"))

# COMMAND ----------

display(dated_df.groupBy("booking_id").count().filter(F.col("count") > 1))
dedup_df = dated_df.dropDuplicates(["booking_id"])
print(dedup_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC E. Window functions and Delta

# COMMAND ----------

movie_revenue_df = (
    dedup_df.filter(F.col("booking_status") == "Confirmed")
    .groupBy("movie_title")
    .agg(F.round(F.sum("net_amount"), 2).alias("net_revenue"))
)
rank_window = Window.orderBy(F.col("net_revenue").desc())
display(movie_revenue_df.withColumn("revenue_rank", F.rank().over(rank_window)))

# COMMAND ----------

final_df = dedup_df.join(cinemas_df, on="cinema_id", how="left")
final_df.write.format("delta").mode("overwrite").saveAsTable("rithika_databricks.default.cinema_bookings_clean")
display(spark.sql("SELECT * FROM rithika_databricks.default.cinema_bookings_clean LIMIT 5"))

# COMMAND ----------

# MAGIC %md
# MAGIC Final Challenge

# COMMAND ----------

report_df = (
    bookings_df
    .dropDuplicates(["booking_id"])
    .fillna({"discount_pct": 0, "payment_method": "Unknown"})
    .filter(F.col("booking_status") == "Confirmed")
    .withColumn("net_amount", F.round(F.col("tickets") * F.col("price_per_ticket") * (1 - F.col("discount_pct") / 100), 2))
    .join(cinemas_df, on="cinema_id", how="left")
    .groupBy(F.col("location.city").alias("city"), "movie_title")
    .agg(
        F.sum("tickets").alias("total_tickets"),
        F.round(F.sum("net_amount"), 2).alias("net_revenue")
    )
    .orderBy(F.col("net_revenue").desc())
)
report_df.write.format("delta").mode("overwrite").saveAsTable("rithika_databricks.default.cinema_performance_report")
display(spark.table("rithika_databricks.default.cinema_performance_report"))