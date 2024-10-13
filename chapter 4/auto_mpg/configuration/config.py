# Data comes from https://www.kaggle.com/datasets/uciml/autompg-dataset
from algorithms.fit_pipeline import (
    evaluate_model,
    preprocess_data,
    split_data,
    train_model,
)
from algorithms.predict import create_prediction_dataframe, make_predictions
from algorithms.select_subset import select_subset
from taipy import Config
from traitlets import default

########################
## Configuration Step ##
########################

dataset_path = "../data/auto-mpg.csv"


# input Data Nodes
auto_data_node_config = Config.configure_csv_data_node(
    id="auto_data", default_path=dataset_path
)
column_subset_config = Config.configure_pickle_data_node(
    id="column_subset",
    default_data=[
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year",
        "origin",
    ],
    default_path="./user_data/subset_list.p",
)

# Intermediate Data Nodes

# Output of subset:
filtered_auto_data_node_config = Config.configure_data_node(id="filtered_auto_df")

# Pipeline training:
X_scaled_node_config = Config.configure_data_node(id="X_scaled")
y_node_config = Config.configure_data_node(id="y")
scaler_node_config = Config.configure_pickle_data_node(
    id="scaler", default_path="./user_data/sclaer.p"
)

X_train_node_config = Config.configure_data_node(id="X_train")
X_test_node_config = Config.configure_data_node(id="X_test")
y_train_node_config = Config.configure_data_node(id="y_train")
y_test_node_config = Config.configure_data_node(id="y_test")

regression_model_node_config = Config.configure_pickle_data_node(
    id="regression_model", default_path="./user_data/model.p"
)

mse_node_config = Config.configure_data_node(id="mse")
r2_node_config = Config.configure_data_node(id="r2")


# Tasks
filter_df_task_config = Config.configure_task(
    id="get_subset",
    function=select_subset,
    input=[auto_data_node_config, column_subset_config],
    output=filtered_auto_data_node_config,
)

preprocess_data_task_config = Config.configure_task(
    id="preprocess_data",
    function=preprocess_data,
    input=filtered_auto_data_node_config,
    output=[X_scaled_node_config, y_node_config, scaler_node_config],
)
split_data_task_config = Config.configure_task(
    id="split_data",
    function=split_data,
    input=[X_scaled_node_config, y_node_config],
    output=[
        X_train_node_config,
        X_test_node_config,
        y_train_node_config,
        y_test_node_config,
    ],
)

train_model_task_config = Config.configure_task(
    id="train_model",
    function=train_model,
    input=[X_train_node_config, y_train_node_config],
    output=regression_model_node_config,
)
evaluate_model_task_config = Config.configure_task(
    id="evaluate_model",
    function=evaluate_model,
    input=[regression_model_node_config, X_test_node_config, y_test_node_config],
    output=[mse_node_config, r2_node_config],
)


# Scenarios
train_auto_pipeline_config = Config.configure_scenario(
    "train_pipeline",
    task_configs=[
        filter_df_task_config,
        preprocess_data_task_config,
        split_data_task_config,
        train_model_task_config,
        evaluate_model_task_config,
    ],
    sequences={
        "filter_sequence": [filter_df_task_config],
        "train_sequence": [
            preprocess_data_task_config,
            split_data_task_config,
            train_model_task_config,
            evaluate_model_task_config,
        ],
    },
)


#########################
## Prediction Scenario ##
#########################

column_subset_predict_config = Config.configure_pickle_data_node(
    id="column_subset_predict",
    default_path="./user_data/subset_list.p",
)

cylinders_node_config = Config.configure_data_node(id="cylinders")
displacement_node_config = Config.configure_data_node(id="displacement")
horsepower_node_config = Config.configure_data_node(id="horsepower")
weight_node_config = Config.configure_data_node(id="weight")
acceleration_node_config = Config.configure_data_node(id="acceleration")
model_year_node_config = Config.configure_data_node(id="modelyear")
origin_node_config = Config.configure_data_node(id="origin")

input_data_node_config = Config.configure_data_node(id="input_data")
predicted_mpg_node_config = Config.configure_data_node(id="predicted_mpg")

use_regression_model_node_config = Config.configure_pickle_data_node(
    id="use_regression_model", default_path="./user_data/model.p"
)

aggregate_input_data_task_config = Config.configure_task(
    id="aggregate_input_data",
    function=create_prediction_dataframe,
    input=[
        column_subset_predict_config,
        cylinders_node_config,
        displacement_node_config,
        horsepower_node_config,
        weight_node_config,
        acceleration_node_config,
        model_year_node_config,
        origin_node_config,
    ],
    output=[input_data_node_config],
)

scaler_predict_node_config = Config.configure_pickle_data_node(
    id="scaler_predict", default_path="./user_data/sclaer.p"
)


predict_task_config = Config.configure_task(
    id="predict",
    function=make_predictions,
    input=[
        use_regression_model_node_config,
        input_data_node_config,
        scaler_predict_node_config,
    ],
    output=predicted_mpg_node_config,
)

predict_config = Config.configure_scenario(
    "predict_mpg",
    task_configs=[aggregate_input_data_task_config, predict_task_config],
)
