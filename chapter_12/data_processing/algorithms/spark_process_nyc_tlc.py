import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, dayofweek, hour, to_date, unix_timestamp, when
from pyspark.sql.types import TimestampType


def read_nyc_tlc_df(file_path: str, spark):
    """Reads a Parquet file into a PySpark DataFrame.
    It handles inconsisten column naming"""
    if file_path and os.path.exists(file_path):
        df = spark.read.parquet(file_path)
        return df.toDF(*[c.lower() for c in df.columns])
    print(f"File not found: {file_path}")
    return None


def _wrangle_nyc_tlc(df):
    df = df.withColumn(
        "tpep_pickup_datetime", col("tpep_pickup_datetime").cast(TimestampType())
    ).withColumn(
        "tpep_dropoff_datetime", col("tpep_dropoff_datetime").cast(TimestampType())
    )

    df = df.fillna(0, subset=["airport_fee", "congestion_surcharge"])
    return df


def _filter_rows(df, year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    return (
        df.filter((col("payment_type") == 1) & (col("total_amount") != 0))
        .filter((col("airport_fee") >= 0) & (col("congestion_surcharge") >= 0))
        .filter(
            (to_date(col("tpep_pickup_datetime")) >= start_date)
            & (to_date(col("tpep_pickup_datetime")) <= end_date)
        )
    )


def _create_features(df):
    return (
        df.withColumn(
            "airport_fee_binary", when(col("airport_fee") > 0, 1).otherwise(0)
        )
        .withColumn(
            "trip_duration",
            (
                unix_timestamp("tpep_dropoff_datetime")
                - unix_timestamp("tpep_pickup_datetime")
            )
            / 60,
        )
        .withColumn(
            "trip_speed_mph",
            when(
                col("trip_duration") > 0,
                col("trip_distance") / (col("trip_duration") / 60),
            ).otherwise(0),
        )
        .withColumn("hour_of_day", hour("tpep_pickup_datetime"))
        .withColumn(
            "is_weekend", dayofweek("tpep_pickup_datetime").isin([1, 7]).cast("integer")
        )
        .withColumn(
            "is_peak_hour",
            when(
                ((col("hour_of_day") >= 7) & (col("hour_of_day") <= 10))
                | ((col("hour_of_day") >= 17) & (col("hour_of_day") <= 20)),
                1,
            ).otherwise(0),
        )
        .withColumn(
            "is_night",
            when((col("hour_of_day") >= 22) | (col("hour_of_day") < 6), 1).otherwise(0),
        )
        .drop("payment_type")
    )


def process_nyc_tlc_df(df, year):
    """Processes NYC TLC data for tipping analysis."""
    df = _wrangle_nyc_tlc(df)
    df = _filter_rows(df, year)
    df = _create_features(df)
    return df


def process_month(spark, month, dataset_name, year, data_folder, output_folder):
    """Processes a single month of data from existing files."""
    file_path = os.path.join(data_folder, f"{dataset_name}_{year}-{month:02d}.parquet")
    df = read_nyc_tlc_df(file_path, spark)
    if df is None:
        return f"Failed to process month {month} - file not found"

    processed_df = process_nyc_tlc_df(df, year)
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(
        output_folder, f"processed_{dataset_name}_{year}_{month:02d}.parquet"
    )
    processed_df.write.mode("overwrite").option(
        "parquet.enable.summary-metadata", "true"
    ).option("compression", "snappy").parquet(output_file)
    return f"Processed data saved: {output_file}"


def process_all_data(
    spark, dataset_name: str, year: int, data_folder: str, output_folder: str
):
    """Orchestrates processing of all specified months."""
    months = list(range(1, 13))
    with ThreadPoolExecutor(max_workers=6) as executor:
        return list(
            executor.map(
                lambda m: process_month(
                    spark, m, dataset_name, year, data_folder, output_folder
                ),
                months,
            )
        )


if __name__ == "__main__":
    # Initialize Spark session when run as script
    spark = (
        SparkSession.builder.appName("NYC TLC Processing")
        .config("spark.sql.shuffle.partitions", "400")
        .config("spark.default.parallelism", "8")
        .getOrCreate()
    )
    spark.conf.set("spark.sql.session.timeZone", "UTC")

    parser = argparse.ArgumentParser(description="Process NYC TLC trip data.")
    parser.add_argument(
        "--dataset",
        default="yellow_tripdata",
        help="Dataset name (e.g., yellow_tripdata)",
    )
    parser.add_argument(
        "--year", type=int, required=True, help="Year of data to process (e.g., 2024)"
    )
    parser.add_argument(
        "--data-folder", default="./data", help="Folder with raw Parquet files"
    )
    parser.add_argument(
        "--output-folder", default="./processed", help="Folder to save processed data"
    )

    args = parser.parse_args()

    print(f"Starting processing: {args.dataset} {args.year}")
    results = process_all_data(
        spark, args.dataset, args.year, args.data_folder, args.output_folder
    )

    for result in results:
        print(result)

    spark.stop()
    sys.exit(0)
