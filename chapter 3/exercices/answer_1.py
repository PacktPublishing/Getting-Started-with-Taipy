import taipy as tp
from taipy import Config, Orchestrator, Scope

## Answer 1 ##

cities_excel_node_config = Config.configure_excel_data_node(
    id="most_populated_cities_excel",
    default_path="../data/cities.xlsx",
    has_header=True,
    exposed_type="numpy",
    scope=Scope.GLOBAL,
)

orchestrator = Orchestrator()
orchestrator.run()
cities_excel_data_node = tp.create_global_data_node(cities_excel_node_config)

dict_cities = cities_excel_data_node.read()

np_cities = dict_cities["cities"]

print("Data from an Excel file as np array:")
print(np_cities)

orchestrator.stop()
