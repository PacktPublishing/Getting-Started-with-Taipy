import datetime as dt

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
    km_prices = {
        "1-2025": 3.95,
        "2-2025": 4,
        "3-2025": 4,
        "4-2025": 4.08,
        "5-2025": 4.08,
        "6-2025": 4.3,
        "7-2025": 4.5,
        "8-2025": 4.5,
        "9-2025": 4.5,
        "10-2025": 4.6,
        "11-2025": 4.4,
        "12-2025": 4.5,
    }

    tp.Orchestrator().run()

    #### For Development: ####
    create_test_scenarios(warehouse_scenario_config)
    ##########################

    selected_scenario = tp.create_scenario(
        warehouse_scenario_config,
        creation_date=dt.datetime(
            2025, 2, 7
        ),  ## Add creation date, or leave empty to use the current datetime
    )
    selected_scenario.name = "Default Scenario"
    selected_scenario.submit()  # Create the default-value scenario so charts are initialized

    scenario_date = f"{selected_scenario.creation_date.month}-{selected_scenario.creation_date.year}"
    km_cost = km_prices.get(scenario_date)
    selected_scenario.price_per_km.write(km_cost)

    df_warehouses = selected_scenario.df_warehouses.read()
    df_customers = selected_scenario.df_customers.read()

    df_selected_warehouses_dn = selected_scenario.df_selected_warehouses
    df_selected_warehouses = df_selected_warehouses_dn.read()
    df_assignments = selected_scenario.df_assignments.read()

    total_price = selected_scenario.total_price.read()
    total_co2 = selected_scenario.total_co2.read()
    total_cost_per_order = selected_scenario.total_cost_per_order.read()
    total_co2_per_order = selected_scenario.total_co2_per_order.read()

    co2_per_km = 2
    optimize = "price"
    country_list = []
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
