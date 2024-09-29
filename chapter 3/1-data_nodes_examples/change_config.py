import taipy as tp
from taipy import Config, Orchestrator, Scope

# Set the DEFAULT Data Node configuration to GLOBAL and CSV
Config.set_default_data_node_configuration(
    storage_type="csv",
    scope=Scope.GLOBAL,
    has_header=True,
)

# Now, you can use the new default Data Node to create CSV Data Nodes
cities_config = Config.configure_data_node(
    id="most_populated_cities_csv",
    default_path="../data/cities.csv",
)


orchestrator = Orchestrator()
orchestrator.run()
cities_csv_data_node = tp.create_global_data_node(cities_config)

df_cities = cities_csv_data_node.read()
print(df_cities.head())
