import os
import subprocess
from pathlib import Path


def run_spark_processing(
    check_download,  # output of previous task
    year=2023,
    script_path="./algorithms/spark_process_nyc_tlc.py",
    data_folder="./data/raw_data",
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

    ########################################data_folder=f"./data/raw_data" #############/{year}"
    ########################################output_folder=f"./data/processed/{year}"

    months_to_process = []
    for month in range(1, 13):
        month_str = str(month).zfill(2)
        file_name = f"processed_yellow_tripdata_{year}_{month_str}.parquet"
        local_path = Path(output_folder) / file_name
        if not local_path.exists():
            months_to_process.append(month)

    if len(months_to_process) == 0:
        print("All files are already processed")
        return 0

    months_str = ",".join(map(str, months_to_process))

    if check_download:
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
            script_path,
            "--year",
            str(year),
            "--data-folder",
            data_folder,
            "--output-folder",
            output_folder,
            "--months",
            months_str,
        ]

        print("Running command:", " ".join(cmd))  # Print the command for debugging

        try:
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print("Spark Job Output:\n", result.stdout)
            return result.returncode
        except subprocess.CalledProcessError as e:
            print("Spark Job Failed!\n")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            print(e.returncode)  # We don't return if error, so we don't cache it
    else:
        print("Download not checked")
        return 1
