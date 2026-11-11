from pyspark import pipelines as dp
from pyspark.sql import functions as F, Window


@dp.table(name="water_py_bronze_readings")
def water_py_bronze_readings():
    return spark.readStream.table("workspace.default.water_meter_readings_source")


@dp.table(name="water_py_silver_readings")
def water_py_silver_readings():
    return (
        spark.readStream.table("water_py_bronze_readings")
        .filter(
            (F.col("reading_status") == "Valid")
            & (F.col("flow_lpm") > 0)
            & (F.col("consumption_liters") > 0)
        )
        .fillna({"source_system": "Unknown"})
    )


@dp.materialized_view(name="water_py_gold_zone_summary")
def water_py_gold_zone_summary():
    latest = Window.partitionBy("reading_id").orderBy(F.col("reading_time").desc())
    silver_df = (
        spark.read.table("water_py_silver_readings")
        .withColumn("rn", F.row_number().over(latest))
        .filter(F.col("rn") == 1)
    )
    zones_df = spark.read.table("workspace.default.water_zones").select("zone_id", "zone_name")
    return (
        silver_df.join(zones_df, "zone_id", "left")
        .groupBy("zone_id", "zone_name")
        .agg(
            F.sum("consumption_liters").alias("total_consumption"),
            F.round(F.avg("pressure_bar"), 2).alias("avg_pressure"),
            F.count("*").alias("reading_count")
        )
    )
