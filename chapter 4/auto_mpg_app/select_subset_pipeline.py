# Data comes from https://www.kaggle.com/datasets/uciml/autompg-dataset
import taipy as tp
from taipy import Config, Orchestrator

########################
## Configuration Step ##
########################

dataset_path = "../data/auto-mpg.csv"


def select_subset(df_auto_mpg, column):
    """Selects a subset of the `df_auto_mpg` DataFrame, including the 'mpg' column and the specified column.

    Args:
        df_auto_mpg (pandas.DataFrame): The original DataFrame containing car data.
        column (str): The name of the column to include in the subset.

    Returns:
        pandas.DataFrame: A new DataFrame containing only the 'mpg' and specified columns.

    Raises:
        ValueError: If the specified column name is not valid.
    """

    if column not in [
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year",
        "origin",
    ]:
        print("The column name is wrong")
        return 1

    dataframe_columns = ["mpg", column]
    df_auto_mpg_filtered = df_auto_mpg[dataframe_columns]
    return df_auto_mpg_filtered


# input Data Nodes
auto_data_node_config = Config.configure_csv_data_node(
    id="auto_data", default_path=dataset_path
)
column_subset_config = Config.configure_data_node(id="column_subset")

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

auto_scenario.column_subset.write("cylinders")

auto_scenario.submit()

df_filtered_auto = auto_scenario.filtered_auto_df.read()

print(df_filtered_auto.head(10))

orchestrator.stop()
