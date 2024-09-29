import taipy as tp
from taipy import Config, Orchestrator, Scope

## Excel File Configuration ##

cities_excel_node_config = Config.configure_excel_data_node(
    id="most_populated_cities_excel",
    default_path="../data/cities.xlsx",
    has_header=True,
    exposed_type="pandas",
    sheet_name="cities",
    scope=Scope.GLOBAL,
)

orchestrator = Orchestrator()
orchestrator.run()
cities_excel_data_node = tp.create_global_data_node(cities_excel_node_config)

df_cities = cities_excel_data_node.read()

print("Data from an Excel file:")
print(df_cities.head(10))

orchestrator.stop()
