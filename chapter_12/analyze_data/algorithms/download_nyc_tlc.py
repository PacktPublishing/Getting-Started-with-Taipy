import os
from pathlib import Path

import boto3


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
