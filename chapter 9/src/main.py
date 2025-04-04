import taipy as tp
import taipy.gui.builder as tgb
from configuration.config import (
    df_paris_parks_node_config,
    gdf_paris_parks_centroids_node_config,
    gdf_paris_parks_node_config,
    ndvi_scenario_config,
)
from create_test_scenarios import create_test_scenarios
from pages.calculate_ndvi.ndvi import ndvi_page
from pages.compare_ndvi.compare_ndvi import compare_page
from pages.general_page.charts import plot_park_with_centroid
from pages.general_page.general_page import general_page
from pages.general_page.park_partial import create_park_info_partial
from taipy.gui import Gui
from update_callbacks import update_compare_selector

with tgb.Page() as root_page:
    with tgb.layout("2 10"):
        tgb.navbar()
        tgb.text("# Paris 🌳 **Parks**", mode="md")


pages = {
    "/": root_page,
    "general_info": general_page,
    "calculate_ndvi": ndvi_page,
    "compare_ndvi": compare_page,
}

stylekit = {"color_primary": "#12b049"}


def on_init(state):
    update_compare_selector(state)
    create_park_info_partial(state)


if __name__ == "__main__":

    tp.Orchestrator().run()

    # Global DataFrames / GeoDataFrames:
    df_paris_parks_node = tp.create_global_data_node(df_paris_parks_node_config)
    df_paris_parks = df_paris_parks_node.read()
    df_paris_parks = df_paris_parks.sort_values(by="name")
    gdf_paris_parks_centroids_node = tp.create_global_data_node(
        gdf_paris_parks_centroids_node_config
    )
    gdf_paris_parks_centroids = gdf_paris_parks_centroids_node.read()

    gdf_paris_parks_node = tp.create_global_data_node(gdf_paris_parks_node_config)
    gdf_paris_parks = gdf_paris_parks_node.read()

    # Scenario Objects
    selected_scenario = create_test_scenarios(ndvi_scenario_config)

    selected_np_tif = selected_scenario.tif_image.read()
    selected_df_time_series = selected_scenario.ndvi_time_series.read()

    selected_scenario_name = selected_scenario.name

    # Count Parks
    number_parks = len(df_paris_parks)
    number_parks_over_100 = df_paris_parks["is_over_100_sqm"].sum()
    number_parks_over_1_000 = df_paris_parks["is_over_1_000_sqm"].sum()

    # Basic stats
    df_types = df_paris_parks.groupby("type").size().reset_index(name="count")
    df_categories = df_paris_parks.groupby("category").size().reset_index(name="count")

    # Values for selectors
    park_ids = df_paris_parks[df_paris_parks["is_over_1_000_sqm"] == 1]["id"].to_list()
    park_names = df_paris_parks[df_paris_parks["is_over_1_000_sqm"] == 1][
        "name"
    ].to_list()
    id_name_list = df_paris_parks[df_paris_parks["is_over_1_000_sqm"] == 1][
        "id_name"
    ].to_list()

    selected_park = id_name_list[0]
    park_id = park_ids[0]
    info_display = "general_info"

    selected_park_row = df_paris_parks[df_paris_parks["id"] == park_id]
    selected_park_dict = selected_park_row.to_dict(orient="records")[0]

    # Values for selectors ndvi scenario
    selected_year = selected_scenario.selected_year.read()
    selected_park_ndvi = id_name_list[0]

    # Values for comparison app
    select_park_name_comp = None
    scenarios_to_compare = []
    scenario_comp_names = [scenario.name for scenario in scenarios_to_compare]
    selected_time_series_list = [
        scenario.ndvi_time_series.read() for scenario in scenarios_to_compare
    ]

    gui = Gui(pages=pages, css_file="./css/main.css")

    park_partial = gui.add_partial(page="")
    compare_partial = gui.add_partial(page="")
    gui.run(
        title="Paris Parks",
        favicon="./img/tree_icon.png",
        dark_mode=False,
        stylekit=stylekit,
        # use_reloader=True,
    )
