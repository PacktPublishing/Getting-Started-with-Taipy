import os

import dask.dataframe as dd


def _concat_dask_year(address, columns):
    """
    Concatenate all parquet datasets (files or directories) from a folder.
    Validates that requested columns exist.
    """
    entries = [os.path.join(address, d) for d in os.listdir(address)]
    parquet_paths = [f for f in entries if f.endswith(".parquet") or os.path.isdir(f)]

    if not parquet_paths:
        raise FileNotFoundError(f"No parquet files or directories found in {address}")
    return dd.concat([dd.read_parquet(p, columns=columns) for p in parquet_paths])


def _calculate_group_stats(ddf, group_col, rename_map=None):
    """
    Group a Dask DataFrame by a specified column and calculate the mean tip amount.
    """
    group = ddf.groupby(group_col).agg({"tip_amount": "mean"})
    group.columns = ["average_tip"]

    if rename_map:
        group = group.reset_index()
        group[group_col] = group[group_col].map(rename_map, meta=(group_col, "object"))
        group = group.set_index(group_col)

    return group


def analyze_tipping_patterns(check_preprocess: bool, address="./data/processed/"):
    """
    Analyze tipping patterns for a given year using Dask.
    Returns aggregated statistics and grouped pandas DataFrames.
    """
    if not check_preprocess:
        raise ValueError("Missing Preprocess step")

    columns_for_analysis = [
        "tip_amount",
        "tpep_pickup_datetime",
        "is_weekend",
        "is_night",
        "hour_of_day",
        "airport_fee_binary",
    ]
    ddf_year = _concat_dask_year(address, columns=columns_for_analysis)

    # Prepare lazy tasks
    tasks = {
        "avg_tip": ddf_year["tip_amount"].mean(),
        "total_trips": ddf_year.shape[0],
        "no_tip_count": ddf_year[ddf_year["tip_amount"] == 0].shape[0],
        "total_tips": ddf_year["tip_amount"].sum(),
    }

    # Group aggregations
    aggregations = {
        "df_weekend": ("is_weekend", {0: "Weekday", 1: "Weekend"}),
        "df_night": ("is_night", {0: "Day", 1: "Night"}),
        "df_hour": ("hour_of_day", None),
        "df_from_airport": ("airport_fee_binary", {0: "No", 1: "Yes"}),
    }
    for key, (col, mapping) in aggregations.items():
        tasks[key] = _calculate_group_stats(ddf_year, col, mapping)

    # Filtered subset
    tip_and_pickup_ddf = ddf_year[["tip_amount", "tpep_pickup_datetime"]].loc[
        (ddf_year["tip_amount"] >= 20) & (ddf_year["tip_amount"] < 100)
    ]
    tasks["tip_and_pickup"] = tip_and_pickup_ddf

    # Compute all at once
    computed_values = dd.compute(*tasks.values())
    results = dict(zip(tasks.keys(), computed_values))

    # Basic metrics
    total_tips = results["total_tips"]
    avg_tip = results["avg_tip"]
    total_trips = results["total_trips"]
    no_tip_count = results["no_tip_count"]
    percentage_no_tip = no_tip_count / total_trips * 100

    # Final DataFrame cleanup
    tip_and_pickup = results["tip_and_pickup"]
    tip_and_pickup["tip_date"] = tip_and_pickup["tpep_pickup_datetime"].astype("int64")
    tip_and_pickup = tip_and_pickup.drop(columns=["tpep_pickup_datetime"])
    tip_and_pickup = tip_and_pickup.reset_index(drop=True)

    result_values = [results[key].reset_index() for key in aggregations.keys()]

    return (
        float(total_tips),
        round(float(avg_tip), 2),
        round(float(percentage_no_tip), 2),
        *result_values,
        tip_and_pickup,
    )
