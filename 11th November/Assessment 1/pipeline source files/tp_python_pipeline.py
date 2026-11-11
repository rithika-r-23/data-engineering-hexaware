from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(name="tp_py_bronze_entries")
def tp_py_bronze_entries():
    return spark.readStream.table("workspace.default.tp_entries_raw")


@dp.table(name="tp_py_silver_entries")
def tp_py_silver_entries():
    return (
        spark.readStream.table("tp_py_bronze_entries")
        .filter(
            (F.col("status") == "Completed")
            & (F.col("wait_minutes") >= 0)
            & (F.col("ride_minutes") > 0)
            & (F.col("ticket_price") > 0)
        )
        .fillna({"booking_channel": "Unknown"})
        .withColumn("ticket_revenue", F.col("ticket_price"))
    )


@dp.materialized_view(name="tp_py_gold_attraction_summary")
def tp_py_gold_attraction_summary():
    silver_df = (
        spark.read.table("tp_py_silver_entries")
        .select("entry_id", "attraction_id", "ticket_revenue")
        .dropDuplicates(["entry_id"])
    )
    attractions_df = spark.read.table("workspace.default.tp_attractions").select("attraction_id", "attraction_name")
    return (
        silver_df.join(attractions_df, "attraction_id", "left")
        .groupBy("attraction_id", "attraction_name")
        .agg(
            F.count("*").alias("completed_entries"),
            F.sum("ticket_revenue").alias("total_revenue")
        )
    )
