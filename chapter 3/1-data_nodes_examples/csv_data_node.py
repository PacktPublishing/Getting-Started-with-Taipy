import taipy as tp
from taipy import Config, Orchestrator, Scope

## Configure a CSV Data Node ##

cities_csv_node_config = Config.configure_csv_data_node(
    id="most_populated_cities_csv",
    default_path="../data/cities.csv",
    has_header=True,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
    cities_csv_data_node = tp.create_global_data_node(cities_csv_node_config)

    df_cities = cities_csv_data_node.read()

    print("Data from a CSV file:")
    print(df_cities.head(10))

    orchestrator.stop()
