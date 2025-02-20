import taipy as tp
from taipy import Config, Orchestrator

########################
## Configuration Step ##
########################

dataset_path = "../data/auto-mpg.csv"


def calculate_column_averages(data):
    """Calculates the average of each numerical column in the given DataFrame.

    Args:
        data: A pandas DataFrame containing the data.

    Returns:
        A dictionary where keys are column names and values are their averages.
    """

    averages = {}
    for column in data.columns:
        if data[column].dtype != "object":  # Check if column is numerical
            average = data[column].mean()
            averages[column] = average
    return averages


def format_averages(averages):
    """Formats the averages dictionary into a string.

    Args:
        averages: A dictionary containing column names and their averages.

    Returns:
        A formatted string displaying each column's average.
    """

    formatted_string = ""
    for column, average in averages.items():
        formatted_string += f"The average of {column} is: {average:.2f}\n"
    return formatted_string


def write_text(data, path):
    with open(path, "w") as text_writer:
        text_writer.write(data)


# input Data Nodes
auto_data_node_config = Config.configure_csv_data_node(
    id="auto_data", default_path=dataset_path
)
averages_data_node_config = Config.configure_data_node(id="averages")

averages_str_data_node_config = Config.configure_generic_data_node(
    id="averages_file", write_fct=write_text, write_fct_args=["./averages.txt"]
)


# Tasks
make_averages_task_config = Config.configure_task(
    id="mak_averages",
    function=calculate_column_averages,
    input=[auto_data_node_config],
    output=averages_data_node_config,
)
make_averages_file_task_config = Config.configure_task(
    id="store_averages",
    function=format_averages,
    input=averages_data_node_config,
    output=averages_str_data_node_config,
)


average_scenario_config = Config.configure_scenario(
    "averages_scenario",
    task_configs=[make_averages_task_config, make_averages_file_task_config],
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()

    averages_scenario = tp.create_scenario(average_scenario_config)

    averages_scenario.submit()

    orchestrator.stop()
