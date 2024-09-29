import taipy.gui.builder as tgb
from pages.data_node_selector import data_node_selector
from pages.data_node_viewer import data_node_viewer
from pages.simple_data_node import simple_data_node
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

data_nodes_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Data Node examples",
)
