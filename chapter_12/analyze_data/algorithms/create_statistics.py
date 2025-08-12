import os

import dask.dataframe as dd


def _concat_dask_year(address, columns):
    parquet_dirs = [os.path.join(address, d) for d in os.listdir(address)]
    return dd.concat(
        [
            dd.read_parquet(f, columns=columns)
            for f in parquet_dirs
            if f.endswith(".parquet")
        ]
    )


def _calculate_basic_metrics(ddf_year):
    """
    Returns Dask objects for basic metric computations without executing them.
    """
    avg_tip = ddf_year["tip_amount"].mean()
    total_trips = ddf_year.shape[0]
    no_tip_count = ddf_year[ddf_year["tip_amount"] == 0].shape[0]
    total_tips = ddf_year["tip_amount"].sum()

    # We do NOT compute here. We return the Dask objects themselves.
    return avg_tip, total_trips, no_tip_count, total_tips


def _calculate_group_stats(ddf, group_col, rename_map=None):
    group = (
        ddf.groupby(group_col)
        .agg({"tip_amount": ["mean"]})
        .rename(columns={"tip_amount": "average_tip"})
    )

    if rename_map:
        group = group.reset_index()
        group[group_col] = group[group_col].map(rename_map)
        group = group.set_index(group_col)

    return group


def analyze_tipping_patterns(
    check_preprocess: bool, address=f"./data/processed/"
) -> dict:
    """
    Analyzes tipping patterns for a given year using Dask.
    Returns aggregated statistics and grouped DataFrames.
    """
    # Read all monthly parquet files for the year
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

    tasks = {
        "avg_tip": ddf_year["tip_amount"].mean(),
        "total_trips": ddf_year.shape[0],
        "no_tip_count": ddf_year[ddf_year["tip_amount"] == 0].shape[0],
        "total_tips": ddf_year["tip_amount"].sum(),
    }

    aggregations = {
        "df_weekend": ("is_weekend", {0: "Weekday", 1: "Weekend"}),
        "df_night": ("is_night", {0: "Day", 1: "Night"}),
        "df_hour": ("hour_of_day", None),
        "df_from_airport": ("airport_fee_binary", {0: "No", 1: "Yes"}),
    }

    for key, (col, mapping) in aggregations.items():
        tasks[key] = _calculate_group_stats(ddf_year, col, mapping)

    tip_and_pickup_ddf = ddf_year[["tip_amount", "tpep_pickup_datetime"]].loc[
        (ddf_year["tip_amount"] >= 20) & (ddf_year["tip_amount"] < 100)
    ]
    tasks["tip_and_pickup"] = tip_and_pickup_ddf

    results = dd.compute(tasks)

    total_tips = results["total_tips"]
    avg_tip = results["avg_tip"]
    total_trips = results["total_trips"]
    no_tip_count = results["no_tip_count"]
    percentage_no_tip = no_tip_count / total_trips * 100

    tip_and_pickup = results["tip_and_pickup"]
    tip_and_pickup["tip_date"] = tip_and_pickup["tpep_pickup_datetime"].astype("int64")
    tip_and_pickup = tip_and_pickup.drop(columns=["tpep_pickup_datetime"])

    result_values = [results[key].reset_index() for key in aggregations.keys()]

    return (
        float(total_tips),
        round(float(avg_tip), 2),
        round(float(percentage_no_tip), 2),
        *result_values,
        tip_and_pickup,
    )
