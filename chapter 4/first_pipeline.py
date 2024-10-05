# Data comes from https://www.kaggle.com/datasets/uciml/autompg-dataset
import pandas as pd
from sklearn.linear_model import LinearRegression
from taipy import Config, Orchestrator

dataset = "./data/auto-mpg.csv"


auto_data_node_config = Config.configure_csv_data_node(
    id="auto_data", default_path=dataset
)
regression_output_data_node = Config.configure_data_node(id="regression_output")


build_msg_task_cfg = Config.configure_task(
    "build_msg", build_message, name_data_node_cfg, message_data_node_cfg
)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])
