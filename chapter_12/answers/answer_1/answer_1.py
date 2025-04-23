import os

import polars as pl  # Install with pip install polars
import taipy as tp
import taipy.gui.builder as tgb
from taipy import Config, Orchestrator
from taipy.gui import Gui


def read_parquet_from_s3_lazy(
    key: str,
    bucket: str = "taipy-nyc-tlc-trip-data",
    aws_access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name: str = "us-east-1",
) -> pl.LazyFrame:
    """
    Reads a Parquet file from an S3 bucket using Polars' scan_parquet.
    It uses Lazy evaluation, so it doesn't load it all in memory.

    Parameters:
        key (str): The object key (path) in the S3 bucket.
        bucket (str): The name of the S3 bucket.
        aws_access_key_id (str, optional): AWS access key ID.
        aws_secret_access_key (str, optional): AWS secret access key.
        region_name (str, optional): AWS region name.

    Returns:
        pl.LazyFrame: A Polars LazyFrame.
    """
    # Construct the S3 URL
    s3_url = f"s3://{bucket}/{key}"

    storage_options = {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_region": region_name,
    }

    # Polar lazy DataFrames can scan files from S3 buckets:
    lazy_df = pl.scan_parquet(s3_url, storage_options=storage_options)
    return lazy_df


def sort_and_get_top20_lazy_input(
    lazy_df: pl.LazyFrame, sort_column: str = "tip_amount"
) -> pl.LazyFrame:
    """
    Sorts the LazyFrame by the specified column using lazy evaluation and limits the result to 20 rows.
    Returns a pandas DataFrame because that's what Taipy uses to create charts and tables.
    Parameters:
        lazy_df (pl.LazyFrame): The Polars LazyFrame to sort.
        sort_column (str): The name of the column to sort by.
        descending (bool): If True, sort in descending order (default is ascending).

    Returns:
        pd.DataFrame: A LazyFrame representing the sorted result limited to 20 rows.
    """
    result_lazy = lazy_df.sort(sort_column, descending=True).limit(20)
    result_polars = result_lazy.collect()

    # Convert to pandas DataFrame
    result_pandas = result_polars.to_pandas()
    return result_pandas


s3_file = "yellow_tripdata_2023-01.parquet"
sort_column = "tip_amount"

read_s3_as_polars_config = Config.configure_generic_data_node(
    id="s3_as_polars",
    read_fct=read_parquet_from_s3_lazy,
    read_fct_args=[s3_file],
)
result_table_node_config = Config.configure_data_node("result_table")
read_20_task = Config.configure_task(
    id="polars_task",
    function=sort_and_get_top20_lazy_input,
    input=read_s3_as_polars_config,
    output=result_table_node_config,
)
polars_scenario_config = Config.configure_scenario("polars_scenario", [read_20_task])


with tgb.Page() as polars_page:
    tgb.text("# Answer 1: Using a custom Polars Data Node", mode="md")
    tgb.data_node("{result_data_node}")


if __name__ == "__main__":

    Orchestrator().run()

    polars_scenario = tp.create_scenario(polars_scenario_config)
    polars_scenario.submit()

    result_data_node = polars_scenario.result_table

    gui = Gui(page=polars_page)
    gui.run(dark_mode=False, use_reloader=True)
