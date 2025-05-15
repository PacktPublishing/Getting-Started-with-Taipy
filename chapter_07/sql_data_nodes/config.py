import os

from algorithms.forecast_tasks import (
    compute_confidence_intervals,
    create_forecast_dataframe,
    filter_dataframe,
    fit_and_forecast_future,
    prepare_data,
    summarize_forecast,
)
from taipy import Config, Scope


def read_query(query_file):
    with open(query_file, "r") as file:
        return file.read()


def dont_write_anything():
    pass


sales_query = read_query("./configuration/sales.sql")
sales_customer_query = read_query("./configuration/sales_customer.sql")
sales_product_query = read_query("./configuration/sales_product.sql")
sales_simplified_query = read_query("./configuration/sales_simplified.sql")

sales_node_config = Config.configure_sql_data_node(
    id="sales_history",
    db_username="postgres",
    db_password=os.getenv("PG_PASSWORD"),
    db_host="localhost",
    db_name="adventure_works_dw",
    db_engine="postgresql",
    db_port="5432",
    read_query=sales_query,
    write_query_builder=dont_write_anything,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

sales_customer_node_config = Config.configure_sql_data_node(
    id="sales_customer",
    db_username="postgres",
    db_password=os.getenv("PG_PASSWORD"),
    db_host="localhost",
    db_name="adventure_works_dw",
    db_engine="postgresql",
    db_port="5432",
    read_query=sales_customer_query,
    write_query_builder=dont_write_anything,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

sales_product_node_config = Config.configure_sql_data_node(
    id="sales_customer",
    db_username="postgres",
    db_password=os.getenv("PG_PASSWORD"),
    db_host="localhost",
    db_name="adventure_works_dw",
    db_engine="postgresql",
    db_port="5432",
    read_query=sales_product_query,
    write_query_builder=dont_write_anything,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)


sales_simplified_node_config = Config.configure_sql_data_node(
    id="sales_simplified",
    db_username="postgres",
    db_password=os.getenv("PG_PASSWORD"),
    db_host="localhost",
    db_name="adventure_works_dw",
    db_engine="postgresql",
    db_port="5432",
    read_query=sales_simplified_query,
    write_query_builder=dont_write_anything,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)


############################
## Forecast configuration ##
############################

### DATA NODES ###
forecast_target_node_config = Config.configure_data_node(
    id="forecast_target",
)
gender_forecast_node_config = Config.configure_data_node(
    id="gender_forecast",
)
generation_forecast_node_config = Config.configure_data_node(
    id="generation_forecast",
)
product_forecast_node_config = Config.configure_data_node(
    id="product_forecast",
)
filtered_dataframe_node_config = Config.configure_data_node(
    id="filtered_dataframe",
)
agg_dataframe_node_config = Config.configure_data_node(
    id="aggregated_dataframe",
)
selected_number_of_days_node_config = Config.configure_data_node(
    id="number_of_days",
)
y_future_node_config = Config.configure_data_node(
    id="y_future",
)
future_dates_node_config = Config.configure_data_node(
    id="future_dates",
)
conf_min_node_config = Config.configure_data_node(
    id="conf_min",
)
conf_max_node_config = Config.configure_data_node(
    id="conf_max",
)
forecast_df_node_config = Config.configure_data_node(
    id="forecast_df",
)
summary_node_config = Config.configure_data_node(
    id="summary",
)

### TASKS ###
filter_task = Config.configure_task(
    id="filter_sales",
    input=[
        sales_simplified_node_config,
        gender_forecast_node_config,
        generation_forecast_node_config,
        product_forecast_node_config,
    ],
    output=filtered_dataframe_node_config,
    function=filter_dataframe,
)
aggregate_task = Config.configure_task(
    id="aggregate_dataframe",
    input=[
        filtered_dataframe_node_config,
        forecast_target_node_config,
    ],
    output=agg_dataframe_node_config,
    function=prepare_data,
)
fit_and_forecast_future_task = Config.configure_task(
    id="fit_and_forecast_future",
    input=[
        agg_dataframe_node_config,
        forecast_target_node_config,
        selected_number_of_days_node_config,
    ],
    output=[y_future_node_config, future_dates_node_config],
    function=fit_and_forecast_future,
)
compute_confidence_intervals_task = Config.configure_task(
    id="compute_confidence_intervals",
    input=y_future_node_config,
    output=[conf_min_node_config, conf_max_node_config],
    function=compute_confidence_intervals,
)
create_forecast_df_task = Config.configure_task(
    id="create_forecast_df",
    input=[
        future_dates_node_config,
        y_future_node_config,
        conf_min_node_config,
        conf_max_node_config,
    ],
    output=forecast_df_node_config,
    function=create_forecast_dataframe,
)
summarize_forecast_task = Config.configure_task(
    id="summarize_forecast",
    input=[forecast_df_node_config],
    output=[summary_node_config],
    function=summarize_forecast,
)

### SCENARIO ###
forecast_scenario_config = Config.configure_scenario(
    id="forecast_scenario",
    task_configs=[
        filter_task,
        aggregate_task,
        fit_and_forecast_future_task,
        compute_confidence_intervals_task,
        create_forecast_df_task,
        summarize_forecast_task,
    ],
)
# This helps document our pipelines:
Config.export("./configuration/config.toml")
