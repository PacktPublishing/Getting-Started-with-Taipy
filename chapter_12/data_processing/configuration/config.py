import datetime as dt

from algorithms.download_nyc_tlc import read_s3
from algorithms.process_nyc_tlc import run_spark_processing
from taipy import Config

check_download_data_node = Config.configure_data_node(
    id="current_date", validity_period=dt.timedelta(days=1)  # Set this for caching
)
check_spark_data_node = Config.configure_data_node(
    id="cache_spark", validity_period=dt.timedelta(days=1)  # Set this for caching
)

########################################
###        Skippable Tasks           ###
########################################
download_task = Config.configure_task(
    "download", function=read_s3, skippable=True, output=check_download_data_node
)
pre_process_task = Config.configure_task(
    "pre_process",
    function=run_spark_processing,
    skippable=True,
    input=check_download_data_node,
    output=check_spark_data_node,
)


download_scenario_config = Config.configure_scenario(
    id="download_files",
    task_configs=[download_task, pre_process_task],
)

Config.export("config.toml")
