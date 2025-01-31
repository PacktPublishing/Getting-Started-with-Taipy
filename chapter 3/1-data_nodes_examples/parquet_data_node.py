import taipy as tp
from taipy import Config, Orchestrator, Scope

## Configure a parquet file ##

cities_parquet_node_config = Config.configure_parquet_data_node(
    id="most_populated_cities_parquet",
    default_path="../data/city_data.parquet",
    engine="pyarrow",  # default
    compression="gzip",  # default is snappy
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
    cities_parquet_data_node = tp.create_global_data_node(cities_parquet_node_config)

    df_cities = cities_parquet_data_node.read()

    print(df_cities.head(10))
