import datetime as dt
import os
from pathlib import Path

import boto3
import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from taipy import Config, Orchestrator
from taipy.gui import Gui


def read_s3(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
    bucket_name="taipy-nyc-tlc-trip-data",  # Replace with your S3 bucket name
    destination_dir="./data/raw_data",
):

    Path(destination_dir).mkdir(parents=True, exist_ok=True)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
    for i in range(1, 13):
        # Format the file name (e.g., file_01.parquet, file_02.parquet, ..., file_12.parquet)
        file_name = f"yellow_tripdata_2023-{i:02d}.parquet"
        s3_key = file_name  # Assuming files are in the root of the bucket
        local_path = Path(destination_dir) / file_name

        if local_path.exists():
            print(f"File already exists, skipping: {local_path}")
            continue  # Skip to the next file

        try:
            # Download the file from S3
            print(f"Downloading {file_name}... {i}/12")
            s3_client.download_file(bucket_name, s3_key, str(local_path))
            print(f"Downloaded {file_name} to {local_path}")
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")

    print("--- Download ended ---")
    return True


current_date_data_node = Config.configure_data_node(
    id="current_date", validity_period=dt.timedelta(days=1)  # Set this for caching
)

########################################
###        Skippable Task            ###
########################################
download_task = Config.configure_task(
    "download", function=read_s3, skippable=True, output=current_date_data_node
)

download_scenario_config = Config.configure_scenario(
    id="download_files",
    task_configs=[download_task],
)


def update_data(state):
    state.df_month = update_month(state.selected_month)


with tgb.Page() as cache_analyze_page:
    tgb.text("# Analyzing and caching some files!", mode="md")

    tgb.selector(
        value="{selected_month}",
        lov=list(range(1, 13)),
        on_change=update_data,
        dropdown=True,
    )

    tgb.table("{df_month}", rebuild=True)

if __name__ == "__main__":

    Orchestrator().run()

    selected_month = 1
    download_scenario = tp.create_scenario(
        download_scenario_config
    )  # , creation_date=dt.datetime(2023, 12, selected_month))

    def update_month(month):
        download_scenario.submit()  # Download data if required
        selected_month_str = str(month).zfill(2)
        df_month = pd.read_parquet(
            f"./data/raw_data/yellow_tripdata_2023-{selected_month_str}.parquet"
        )
        # check_download = download_scenario.current_date.read()
        return df_month

    df_month = update_month(selected_month)

    gui = Gui(page=cache_analyze_page)

    gui.run(dark_mode=False, use_reloader=True)
