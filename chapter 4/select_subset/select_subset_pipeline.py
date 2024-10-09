# Data comes from https://www.kaggle.com/datasets/uciml/autompg-dataset
from email.policy import default

import taipy as tp
from taipy import Config, Orchestrator

########################
## Configuration Step ##
########################

dataset_path = "../data/auto-mpg.csv"


def select_subset(df_auto_mpg, columns):
    """Selects a subset of the `df_auto_mpg` DataFrame, including the 'mpg' column and the specified columns.

    Args:
        df_auto_mpg (pandas.DataFrame): The original DataFrame containing car data.
        columns (list[str]): A list of column names to include in the subset.

    Returns:
        pandas.DataFrame: A new DataFrame containing only the 'mpg' and specified columns.

    Raises:
        ValueError: If any of the specified column names are not valid.
    """

    valid_columns = [
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year",
        "origin",
        "car name",
    ]

    for column in columns:
        if column not in valid_columns:
            raise ValueError(f"Invalid column name: {column}")

    dataframe_columns = ["mpg"] + columns
    df_auto_mpg_filtered = df_auto_mpg[dataframe_columns]
    return df_auto_mpg_filtered


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


filter_df_task_config = Config.configure_task(
    id="get_subset",
    function=select_subset,
    input=[auto_data_node_config, column_subset_config],
    output=filtered_auto_data_node_config,
)

auto_scenario_config = Config.configure_scenario(
    "auto_scenario", task_configs=[filter_df_task_config]
)


orchestrator = Orchestrator()
orchestrator.run()

auto_scenario = tp.create_scenario(auto_scenario_config)

# auto_scenario.column_subset.write(["cylinders", "horsepower"])  # override if you want

auto_scenario.submit()

df_filtered_auto = auto_scenario.filtered_auto_df.read()

print(df_filtered_auto.head(10))

orchestrator.stop()
