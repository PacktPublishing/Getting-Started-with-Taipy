import os

import dask.dataframe as dd


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

    parquet_dirs = [os.path.join(address, d) for d in os.listdir(address)]
    ddf_year = dd.concat(
        [dd.read_parquet(f) for f in parquet_dirs if f.endswith(".parquet")]
    )

    # Calculate basic metrics
    results = dd.compute(
        ddf_year["tip_amount"].mean(),
        ddf_year.shape[0],
        ddf_year[ddf_year["tip_amount"] == 0].shape[0],
        ddf_year["tip_amount"].sum(),
    )
    avg_tip, total_trips, no_tip_count, total_tips = results
    percentage_no_tip = no_tip_count / total_trips * 100

    # # Grouping functions
    def calculate_group_stats(group_col, rename_map=None):
        group = ddf_year.groupby(group_col).agg({"tip_amount": ["mean"]}).compute()
        group.columns = ["average_tip"]
        group = group.reset_index()
        if rename_map:
            group[group_col] = group[group_col].map(rename_map)
        return group

    # # Create all grouped dataframes
    aggregations = {
        "df_weekend": ("is_weekend", {0: "Weekday", 1: "Weekend"}),
        "df_night": ("is_night", {0: "Day", 1: "Night"}),
        "df_hour": ("hour_of_day", None),
        "df_from_airport": ("airport_fee_binary", {0: "No", 1: "Yes"}),
    }

    results = {}
    for key, (col, mapping) in aggregations.items():
        results[key] = calculate_group_stats(col, mapping)

    tip_and_pickup = ddf_year[["tip_amount", "tpep_pickup_datetime"]].compute()

    # Convert datetime to date format (memory-efficient and easier to plot!)
    tip_and_pickup["tip_date"] = tip_and_pickup["tpep_pickup_datetime"].astype("int64")
    tip_and_pickup = tip_and_pickup.drop(columns=["tpep_pickup_datetime"])

    tip_and_pickup = tip_and_pickup.loc[
        (tip_and_pickup["tip_amount"] >= 20) & (tip_and_pickup["tip_amount"] < 100)
    ]

    result_values = list(results.values())
    return (
        float(total_tips),
        round(float(avg_tip), 2),
        round(float(percentage_no_tip), 2),
        *result_values,
        tip_and_pickup,
    )
