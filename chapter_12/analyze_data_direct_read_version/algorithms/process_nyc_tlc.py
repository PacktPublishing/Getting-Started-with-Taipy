import os
import subprocess
from pathlib import Path


def run_spark_processing(
    year=2023,
    script_path="./algorithms/spark_process_nyc_tlc.py",
    data_folder="s3a://taipy-nyc-tlc-trip-data",  # S3 Bucket to read from
    output_folder="./data/processed",
    executor_cores=6,
    master="local[*]",
    driver_memory="4G",
    executor_memory="4G",
):
    """
    Runs the Spark script using subprocess, simulating a CLI execution.

    Parameters:
    - script_path (str): Path to the Spark script (.py file).
    #####################################################################- year (int): Year of data to process.
    - data_folder (str): Directory containing raw parquet files.
    - output_folder (str): Directory to save processed data.
    - master (str): Spark master URL (e.g., "local[*]" or "yarn").
    - driver_memory (str): Memory allocation for the driver.
    - executor_memory (str): Memory allocation per executor.
    - executor_cores (int): Number of CPU cores per executor.

    Returns:
    - int: Exit code of the process (0 if successful, non-zero if error).
    """

    os.makedirs(output_folder, exist_ok=True)
    cmd = [
        "spark-submit",
        "--master",
        master,
        "--deploy-mode",
        "client",
        "--driver-memory",
        driver_memory,
        "--executor-memory",
        executor_memory,
        "--executor-cores",
        str(executor_cores),
        # Add these lines to read from S3 Bucket ### WARNING: look at what verson work best for you
        "--packages",
        "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.367",
        "--conf",
        "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
        "--conf",
        "spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.EnvironmentVariableCredentialsProvider",
        # ---------------------- #
        script_path,
        "--year",
        str(year),
        "--data-folder",
        data_folder,
        "--output-folder",
        output_folder,
    ]

    print("Running command:", " ".join(cmd))  # Print the command for debugging

    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print("Spark Job Output:\n", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Spark Job Failed!\n")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        print(e.returncode)  # We don't return if error, so we don't cache it
