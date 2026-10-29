
import os
import sys
from pathlib import Path


os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import DateType, IntegerType, StringType, StructField, StructType

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = HERE / "output"

THRESHOLD_PCT = 25.0

MOVEMENT_SCHEMA = StructType([
    StructField("movement_id", IntegerType(), False),
    StructField("product_id", IntegerType(), False),
    StructField("warehouse_id", IntegerType(), False),
    StructField("movement_type", StringType(), True),
    StructField("quantity", IntegerType(), False),
    StructField("movement_date", DateType(), True),
    StructField("reference_no", StringType(), True),
    StructField("reason", StringType(), True),
])


def main():
    spark = (SparkSession.builder.appName("WarehouseInsights").master("local[*]")
             .config("spark.sql.shuffle.partitions", "8")
             .config("spark.ui.showConsoleProgress", "false").getOrCreate())
    spark.sparkContext.setLogLevel("WARN")

    
    movements = spark.read.csv((PROCESSED_DIR / "stock_movements_clean.csv").as_uri(),
                               header=True, schema=MOVEMENT_SCHEMA)
    products = spark.read.csv((RAW_DIR / "products.csv").as_uri(), header=True, inferSchema=True)
    warehouses = spark.read.csv((RAW_DIR / "warehouses.csv").as_uri(), header=True, inferSchema=True)
    print(f"Movements loaded: {movements.count():,} rows")

    
    stock = movements.groupBy("product_id", "warehouse_id").agg(
        F.sum("quantity").alias("quantity_on_hand"),
        F.max("movement_date").alias("last_movement_date"))

    detail = (stock.join(F.broadcast(products), "product_id")
              .join(F.broadcast(warehouses.select("warehouse_id", "warehouse_name", "city")), "warehouse_id")
              .withColumn("stock_status",
                          F.when(F.col("quantity_on_hand") < F.col("reorder_level"), "LOW_STOCK")
                           .when(F.col("quantity_on_hand") > F.col("max_stock_level"), "OVERSTOCK")
                           .otherwise("OK"))
              .withColumn("stock_value", F.col("quantity_on_hand") * F.col("unit_price")))
    detail.cache()

    
    warehouse_status = (detail.groupBy("warehouse_id", "warehouse_name", "city").agg(
            F.sum("quantity_on_hand").alias("total_units"),
            F.round(F.sum("stock_value"), 2).alias("total_stock_value"),
            F.count("*").alias("product_lines"),
            F.sum(F.when(F.col("stock_status") == "LOW_STOCK", 1).otherwise(0)).alias("low_stock_items"),
            F.sum(F.when(F.col("stock_status") == "OVERSTOCK", 1).otherwise(0)).alias("overstock_items"))
        .withColumn("low_stock_pct", F.round(100 * F.col("low_stock_items") / F.col("product_lines"), 1))
        .withColumn("overstock_pct", F.round(100 * F.col("overstock_items") / F.col("product_lines"), 1))
        .withColumn("warehouse_status",
                    F.when((F.col("low_stock_pct") >= THRESHOLD_PCT) &
                           (F.col("low_stock_pct") >= F.col("overstock_pct")), "UNDERSTOCKED")
                     .when(F.col("overstock_pct") >= THRESHOLD_PCT, "OVERSTOCKED")
                     .otherwise("BALANCED"))
        .orderBy("warehouse_id"))

    
    exceptions = (detail.filter(F.col("stock_status") != "OK")
                  .select("warehouse_id", "warehouse_name", "product_id", "sku", "product_name", "category",
                          "quantity_on_hand", "reorder_level", "max_stock_level", "stock_status")
                  .orderBy("warehouse_id", "stock_status", "product_id"))


    category_status = (detail.groupBy("warehouse_name", "category").agg(
            F.sum("quantity_on_hand").alias("total_units"),
            F.sum(F.when(F.col("stock_status") == "LOW_STOCK", 1).otherwise(0)).alias("low_stock_items"),
            F.sum(F.when(F.col("stock_status") == "OVERSTOCK", 1).otherwise(0)).alias("overstock_items"))
        .orderBy("warehouse_name", "category"))

    print("\nWAREHOUSE-LEVEL STOCK STATUS")
    warehouse_status.show(truncate=False)
    print("SAMPLE ITEM EXCEPTIONS")
    exceptions.show(10, truncate=False)


    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    warehouse_status.toPandas().to_csv(OUTPUT_DIR / "warehouse_stock_status.csv", index=False)
    exceptions.toPandas().to_csv(OUTPUT_DIR / "warehouse_item_exceptions.csv", index=False)
    category_status.toPandas().to_csv(OUTPUT_DIR / "warehouse_category_status.csv", index=False)
    print(f"Saved results to {OUTPUT_DIR}")

    spark.stop()


if __name__ == "__main__":
    main()
