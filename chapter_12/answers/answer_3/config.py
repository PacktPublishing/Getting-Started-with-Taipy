import datetime as dt

from algorithms.create_statistics import analyze_tipping_patterns
from algorithms.download_nyc_tlc import read_s3
from algorithms.process_nyc_tlc import run_spark_processing

from taipy import Config

check_download_data_node_config = Config.configure_data_node(
    id="current_date", validity_period=dt.timedelta(days=1)  # Set this for caching
)
check_spark_data_node_config = Config.configure_data_node(
    id="cache_spark", validity_period=dt.timedelta(days=1)  # Set this for caching
)

total_tips_data_node_config = Config.configure_data_node(
    id="total_tips", validity_period=dt.timedelta(days=1)  # Set this for caching
)
avg_tip_data_node_config = Config.configure_data_node(
    id="avg_tip", validity_period=dt.timedelta(days=1)  # Set this for caching
)
percentage_no_tip_data_node_config = Config.configure_data_node(
    id="percentage_no_tip", validity_period=dt.timedelta(days=1)  # Set this for caching
)
df_weekend_data_node_config = Config.configure_data_node(
    id="df_weekend", validity_period=dt.timedelta(days=1)  # Set this for caching
)
df_night_data_node_config = Config.configure_data_node(
    id="df_night", validity_period=dt.timedelta(days=1)  # Set this for caching
)
df_hour_data_node_config = Config.configure_data_node(
    id="df_hour", validity_period=dt.timedelta(days=1)  # Set this for caching
)
df_from_airport_data_node_config = Config.configure_data_node(
    id="df_from_airport", validity_period=dt.timedelta(days=1)  # Set this for caching
)
tip_and_pickup_data_node_config = Config.configure_data_node(
    id="tip_and_pickup", validity_period=dt.timedelta(days=1)  # Set this for caching
)
## For answer 3:
df_location_data_node_config = Config.configure_data_node(
    id="df_location", validity_period=dt.timedelta(days=1)  # Set this for caching
)
########################################
###              Tasks               ###
########################################
download_task = Config.configure_task(
    "download", function=read_s3, skippable=True, output=check_download_data_node_config
)
pre_process_task = Config.configure_task(
    "pre_process",
    function=run_spark_processing,
    skippable=True,
    input=check_download_data_node_config,
    output=check_spark_data_node_config,
)
analyze_task = Config.configure_task(
    "analyze",
    function=analyze_tipping_patterns,
    skippable=True,
    input=check_spark_data_node_config,
    output=[
        total_tips_data_node_config,
        avg_tip_data_node_config,
        percentage_no_tip_data_node_config,
        df_weekend_data_node_config,
        df_night_data_node_config,
        df_hour_data_node_config,
        df_from_airport_data_node_config,
        tip_and_pickup_data_node_config,
        df_location_data_node_config,  # For Answer 3
    ],
)

analyze_scenario_config = Config.configure_scenario(
    id="download_files",
    task_configs=[download_task, pre_process_task, analyze_task],
)

Config.export("config.toml")
