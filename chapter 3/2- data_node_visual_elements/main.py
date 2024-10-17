import taipy as tp
import taipy.gui.builder as tgb
from configuration.config_data_nodes import (
    cities_csv_node_config,
    world_countries_area_config,
    world_countries_pop_config,
)
from pages.data_node_selector import data_node_selector
from pages.data_node_viewer import data_node_viewer
from pages.simple_data_node import simple_data_node
from taipy import Orchestrator
from taipy.gui import Gui

with tgb.Page() as root_page:
    tgb.text("# Taipy Data Nodes", mode="md")
    tgb.navbar()

data_nodes_pages = {
    "/": root_page,
    "simple_data_node": simple_data_node,
    "data_node_selector": data_node_selector,
    "data_node_viewer": data_node_viewer,
}


data_nodes_gui = Gui(pages=data_nodes_pages)

if __name__ == "__main__":

    orchestrator = Orchestrator()
    orchestrator.run()

    world_countries_area = tp.create_global_data_node(world_countries_area_config)
    world_countries_pop = tp.create_global_data_node(world_countries_pop_config)
    biggest_cities = tp.create_global_data_node(cities_csv_node_config)

    selected_data_node = world_countries_area

    df_cities = biggest_cities.read()

    data_nodes_gui.run(
        use_reloader=True,
        dark_mode=False,
        title="Data Node examples",
    )
