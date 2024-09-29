import taipy as tp
from taipy import Config, Core, Scope

## Answer 1 ##

cities_excel_node_config = Config.configure_excel_data_node(
    id="most_populated_cities_excel",
    default_path="./data/cities.xlsx",
    has_header=True,
    exposed_type="numpy",
    scope=Scope.GLOBAL,
)

core = Core()
core.run()
cities_excel_data_node = tp.create_global_data_node(cities_excel_node_config)

dict_cities = cities_excel_data_node.read()
np_cities = sheet_name = dict_cities["cities"]
np_cities = cities_excel_data_node.read()

print("Data from an Excel file as np array:")
print(np_cities)

core.stop()
