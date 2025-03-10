import taipy as tp
from taipy import Config, Orchestrator, Scope

## Configure a Pickle Data Node ##

cities_pickle_node_config = Config.configure_pickle_data_node(
    id="most_populated_cities_pickle",
    default_path="../data/cities.p",
    scope=Scope.GLOBAL,
)

tokyo_pickle_node_config = Config.configure_pickle_data_node(
    id="tokyo_data_node",
    default_data="Tokyo",
    scope=Scope.GLOBAL,
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
    cities_pickle_data_node = tp.create_global_data_node(cities_pickle_node_config)
    df_cities = cities_pickle_data_node.read()

    print("Data from a pickle file:")
    print(df_cities.head(10))

    tokyo_pickle_data_node = tp.create_global_data_node(tokyo_pickle_node_config)
    tokyo = tokyo_pickle_data_node.read()
    print(
        """Data from a declarative pickle object
        (biggest city in the world):"""
    )
    print(tokyo)

    orchestrator.stop()
