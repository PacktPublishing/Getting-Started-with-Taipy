import json  # To better display

import taipy as tp
from taipy import Config, Core, Scope

## Configure a JSON Data Node ##

cities_json_node_config = Config.configure_json_data_node(
    id="most_populated_cities_json",
    default_path="./data/cities.json",
    scope=Scope.GLOBAL,
)


core = Core()
core.run()
cities_json_data_node = tp.create_global_data_node(cities_json_node_config)

cities = cities_json_data_node.read()

print("Data from a JSON file:")
print(json.dumps(cities, indent=4))
print(type(cities))

core.stop()
