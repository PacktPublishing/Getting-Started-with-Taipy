from configuration.config import warehouse_scenario_config
from create_test_scenarios import create_test_scenarios
from pages import *

import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Gui

with tgb.Page() as root_page:
    with tgb.layout("10 1 1"):
        tgb.navbar()
        tgb.text("# **EuroDuctPipe**", mode="md")
        tgb.image("./img/logo_nbg.png", width="100px")

pages = {
    "/": root_page,
    "analysis": analysis_page,
    "scenario": scenario_page,
    "comparison": comparison_page,
    "admin": admin_page,
}

stylekit = {"color_primary": "#003399"}


if __name__ == "__main__":

    tp.Orchestrator().run()

    #### For Development: ####
    create_test_scenarios(warehouse_scenario_config)
    ##########################

    selected_scenario = tp.create_scenario(warehouse_scenario_config)
    selected_scenario.name = "Default Scenario"
    selected_scenario.submit()  # Create the default-value scenario so charts are initialized

    df_warehouses = selected_scenario.df_warehouses.read()
    df_customers = selected_scenario.df_customers.read()

    df_selected_warehouses_dn = selected_scenario.df_selected_warehouses
    df_selected_warehouses = df_selected_warehouses_dn.read()
    df_assignments = selected_scenario.df_assignments.read()

    total_price = selected_scenario.total_price.read()
    total_co2 = selected_scenario.total_co2.read()
    total_cost_per_order = selected_scenario.total_cost_per_order.read()
    total_co2_per_order = selected_scenario.total_co2_per_order.read()

    price_per_km = 4
    co2_per_km = 2
    optimize = "price"
    country_list = []
    no_country_list = []  ################### Add this for answer 3
    number_of_warehouses = "any"
    all_countries = df_warehouses["country"].unique()

    active_scenario = True
    # Read file to display text:
    with open("./pages/scenario/scenario_description.md") as sc_desc:
        scenario_description_md = sc_desc.read()

    # For the admin page:
    admin_scenarios = tp.get_scenarios()
    admin_scenario = admin_scenarios[0]  # Get one to initialize

    admin_data_nodes = tp.get_data_nodes()
    admin_data_node = admin_data_nodes[0]

    gui = Gui(pages=pages, css_file="./css/main.css")
    gui.run(
        title="EuroDuctPipe",
        favicon="./img/favicon.png",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
