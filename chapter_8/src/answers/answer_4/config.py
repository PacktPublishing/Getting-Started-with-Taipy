import datetime as dt

from algorithmns.algos import (
    calculate_distance_matrix,
    calculate_total_numbers,
    create_pulp_model,
)
from taipy import Config, Frequency, Scope

###################################
###         Data Nodes          ###
###################################
warehouses_data_node_config = Config.configure_csv_data_node(
    id="df_warehouses", default_path="./data/warehouses.csv", scope=Scope.GLOBAL
)
customers_data_node_config = Config.configure_csv_data_node(
    id="df_customers", default_path="./data/customers.csv", scope=Scope.GLOBAL
)
distance_matrix_data_node_config = Config.configure_data_node(
    id="distance_matrix", scope=Scope.GLOBAL, validity_period=dt.timedelta(days=1)
)

optimize_data_node = Config.configure_data_node(
    id="optimization_target",
    default_data="price",
)
number_of_warehouses_data_node_config = Config.configure_data_node(
    id="number_of_warehouses", default_data="any"
)
country_list_data_node_config = Config.configure_data_node(
    id="country_list", default_data=[]
)
price_per_km_data_node_config = Config.configure_data_node(
    id="price_per_km", default_data=4, scope=Scope.CYCLE
)

co2_per_km_data_node_config = Config.configure_data_node(
    id="co2_per_km", default_data=2
)

df_selected_warehouses_node_config = Config.configure_csv_data_node(
    id="df_selected_warehouses",
)
df_assignments_node_config = Config.configure_csv_data_node(
    id="df_assignments",
)

total_price_node_config = Config.configure_data_node(id="total_price")
total_co2_node_config = Config.configure_data_node(id="total_co2")
total_cost_per_order_node_config = Config.configure_data_node(id="total_cost_per_order")
total_co2_per_order_node_config = Config.configure_data_node(id="total_co2_per_order")

###################################
###           Tasks             ###
###################################

compute_distance_matrix_task_config = Config.configure_task(
    id="compute_distance_matrix",
    function=calculate_distance_matrix,
    input=[warehouses_data_node_config, customers_data_node_config],
    output=distance_matrix_data_node_config,
    skippable=True,
)
create_pulp_model_task_config = Config.configure_task(
    id="pulp_model",
    function=create_pulp_model,
    input=[
        warehouses_data_node_config,
        customers_data_node_config,
        distance_matrix_data_node_config,
        optimize_data_node,
        number_of_warehouses_data_node_config,
        country_list_data_node_config,
        price_per_km_data_node_config,
        co2_per_km_data_node_config,
    ],
    output=[df_selected_warehouses_node_config, df_assignments_node_config],
)
calculate_total_numbers_task_config = Config.configure_task(
    id="calculate_total_numbers",
    function=calculate_total_numbers,
    input=df_selected_warehouses_node_config,
    output=[
        total_price_node_config,
        total_co2_node_config,
        total_cost_per_order_node_config,
        total_co2_per_order_node_config,
    ],
)

###################################
###         Scenario            ###
###################################

warehouse_scenario_config = Config.configure_scenario(
    id="warehouse_scenario",
    task_configs=[
        compute_distance_matrix_task_config,
        create_pulp_model_task_config,
        calculate_total_numbers_task_config,
    ],
    frequency=Frequency.MONTHLY,
)
Config.export("config.toml")
