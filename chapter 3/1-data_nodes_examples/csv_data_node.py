import taipy as tp
from taipy import Config, Core, Scope

## CSV ##

cities_csv_node_config = Config.configure_csv_data_node(
    id="most_populated_cities_csv",
    default_path="./data/cities.csv",
    has_header=True,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

core = Core()
core.run()
cities_csv_data_node = tp.create_global_data_node(cities_csv_node_config)

df_cities = cities_csv_data_node.read()

print("Data from a CSV file:")
print(df_cities.head())

core.stop()
