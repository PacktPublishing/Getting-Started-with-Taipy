import taipy as tp
from configuration.config_data_nodes import (
    cities_csv_node_config,
    world_countries_area_config,
    world_countries_pop_config,
)
from taipy import Orchestrator

orchestrator = Orchestrator()
orchestrator.run()

world_countries_area = tp.create_global_data_node(world_countries_area_config)
world_countries_pop = tp.create_global_data_node(world_countries_pop_config)
biggest_cities = tp.create_global_data_node(cities_csv_node_config)
