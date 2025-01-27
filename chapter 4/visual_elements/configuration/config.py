# Data comes from https://www.kaggle.com/datasets/uciml/autompg-dataset
from algorithms.select_subset import select_subset
from taipy import Config

########################
## Configuration Step ##
########################

dataset_path = "../data/auto-mpg.csv"


# input Data Nodes
auto_data_node_config = Config.configure_csv_data_node(
    id="auto_data", default_path=dataset_path
)
column_subset_config = Config.configure_data_node(
    id="column_subset",
    default_data=[
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year",
        "origin",
        "car name",
    ],
)

# Output Data Node
filtered_auto_data_node_config = Config.configure_data_node(id="filtered_auto_df")

# Tasks
filter_df_task_config = Config.configure_task(
    id="get_subset",
    function=select_subset,
    input=[auto_data_node_config, column_subset_config],
    output=filtered_auto_data_node_config,
)

# Scenarios
auto_scenario_config = Config.configure_scenario(
    "auto_scenario", task_configs=[filter_df_task_config]
)
