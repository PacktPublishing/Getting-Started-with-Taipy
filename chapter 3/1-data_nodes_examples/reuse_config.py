import taipy as tp
from taipy import Config, Orchestrator, Scope

## Configure a CSV Data Node ##

cities_csv_node_pandas_config = Config.configure_csv_data_node(
    id="most_populated_cities_df",
    default_path="../data/cities.csv",
    has_header=True,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

cities_csv_node_numpy_config = Config.configure_data_node_from(
    cities_csv_node_pandas_config,
    id="most_populated_cities_np",
    exposed_type="numpy",
)

orchestrator = Orchestrator()
orchestrator.run()
cities_pandas_data_node = tp.create_global_data_node(cities_csv_node_pandas_config)
cities_numpy_data_node = tp.create_global_data_node(cities_csv_node_numpy_config)

df_cities = cities_pandas_data_node.read()

print("Data as a Pandas DataFrame:")
print(df_cities.head(10))

np_cities = cities_numpy_data_node.read()
print("Data as a Numpy array:")
print(np_cities)
orchestrator.stop()
