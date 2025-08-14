import os
from pathlib import Path

import dask.dataframe as dd
import pyarrow.parquet as pq
from dask.distributed import Client


def _wrangle_nyc_tlc(df):
    df.columns = df.columns.str.lower()
    df = df.assign(
        tpep_pickup_datetime=dd.to_datetime(df.tpep_pickup_datetime),
        tpep_dropoff_datetime=dd.to_datetime(df.tpep_dropoff_datetime),
    )
    df = df.fillna({"airport_fee": 0, "congestion_surcharge": 0})
    return df


def _filter_rows(df, year):
    df = df[(df.payment_type == 1) & (df.total_amount != 0)]
    df = df[(df.airport_fee >= 0) & (df.congestion_surcharge >= 0)]
    df = df[df.tpep_pickup_datetime.dt.year == year]
    return df


def _create_features(df):
    df = df.assign(
        airport_fee_binary=(df.airport_fee > 0).astype(int),
        trip_duration=(
            df.tpep_dropoff_datetime - df.tpep_pickup_datetime
        ).dt.total_seconds()
        / 60,
    )
    df = df = df.assign(
        trip_speed_mph=(df.trip_distance / (df.trip_duration / 60)).where(
            df.trip_duration > 0, 0
        )
    )
    df = df.assign(
        hour_of_day=df.tpep_pickup_datetime.dt.hour,
        is_weekend=df.tpep_pickup_datetime.dt.dayofweek.isin([5, 6]).astype(int),
    )
    df = df.assign(
        is_peak_hour=(
            ((df.hour_of_day >= 7) & (df.hour_of_day <= 10))
            | ((df.hour_of_day >= 17) & (df.hour_of_day <= 20))
        ).astype(int)
    )
    df = df.assign(is_night=((df.hour_of_day >= 22) | (df.hour_of_day < 6)).astype(int))
    return df


def process_nyc_tlc_df(df, year):
    """Processes NYC TLC data for tipping analysis."""
    df = _wrangle_nyc_tlc(df)
    df = _filter_rows(df, year)
    df = _create_features(df)

    df = df.drop("payment_type", axis=1)
    return df


def _select_columns(file_path):
    """This function exists because the original dataset
    has inconsistent naming in the columns
    eg: airport_fee in 01/2023 and Airport_fee in 02/2023
    """
    schema = pq.read_schema(file_path)
    columns_to_select = {
        "tip_amount",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "payment_type",
        "total_amount",
        "airport_fee",
        "congestion_surcharge",
        "trip_distance",
    }
    return [column for column in schema.names if column.lower() in columns_to_select]


def process_month(month, dataset_name, year, data_folder, output_folder):
    """Read, process, and write one month of data."""
    file_path = os.path.join(data_folder, f"{dataset_name}_{year}-{month:02d}.parquet")
    if not os.path.exists(file_path):
        print(f"Missing file for month {month}")
        return None
    selected_columns = _select_columns(file_path)
    df = dd.read_parquet(file_path, columns=selected_columns)
    processed_df = process_nyc_tlc_df(df, year)
    output_file = os.path.join(
        output_folder, f"processed_{dataset_name}_{year}_{month:02d}.parquet"
    )
    processed_df.to_parquet(output_file, compression="snappy", write_metadata_file=True)
    print(f"Processed month {month}")
    return output_file


def all_data_is_processed(
    output_folder: Path, year: int, expected_count: int = 12
) -> bool:
    search_pattern = f"processed_yellow_tripdata_{year}_*"
    matching_folders = list(output_folder.glob(search_pattern))
    if len(matching_folders) == expected_count:
        print("skipping Dask Task - All files exist")
        return True
    return False


def process_nyc_tlc(
    check_download,
    year=2023,
    dataset_name="yellow_tripdata",
    data_folder="./data/raw_data",
    output_folder="./data/processed",
    max_workers=2,
    threads_per_worker=1,
):
    """Run month processing in parallel using Dask's distributed scheduler."""
    if not check_download:
        return "Download not checked"

    os.makedirs(output_folder, exist_ok=True)
    if all_data_is_processed(Path(output_folder), year):
        return True

    # Start local Dask cluster with N workers
    client = Client(
        n_workers=max_workers,
        threads_per_worker=threads_per_worker,
    )
    print(f"Dask dashboard: {client.dashboard_link}")

    months = list(range(1, 13))
    futures = []
    for month in months:
        futures.append(
            client.submit(
                process_month,
                month,
                dataset_name,
                year,
                data_folder,
                output_folder,
            )
        )

    results = client.gather(futures)
    client.close()

    print("All months processed.")
    return results
