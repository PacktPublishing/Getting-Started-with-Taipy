# Answer 5
# --------------
# Move the directory to the /pages directory, and don't forget to import the page!
#

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import notify


def refresh_all_scenarios(state):
    notify(state, "info", "Comparing all the scenarios...")
    scenarios = tp.get_scenarios()
    create_comparison_df(state, scenarios)


def create_comparison_df(state, scenarios):
    scenario_names = [scenario.name for scenario in scenarios]

    scenario_target = [scenario.optimization_target.read() for scenario in scenarios]
    scenario_number_of_warehouses = [
        scenario.number_of_warehouses.read() for scenario in scenarios
    ]
    scenario_country_list = [scenario.country_list.read() for scenario in scenarios]
    scenario_price_per_km = [scenario.price_per_km.read() for scenario in scenarios]
    scenario_co2_per_km = [scenario.co2_per_km.read() for scenario in scenarios]

    scenario_costs = [scenario.total_price.read() for scenario in scenarios]
    scenario_co2 = [scenario.total_co2.read() for scenario in scenarios]
    scenario_total_cost_per_order = [
        scenario.total_cost_per_order.read() for scenario in scenarios
    ]
    scenario_total_co2_per_order = [
        scenario.total_co2_per_order.read() for scenario in scenarios
    ]
    df_comparison = pd.DataFrame(
        {
            "scenario_name": scenario_names,
            "optimization_target": scenario_target,
            "number_of_warehouses": scenario_number_of_warehouses,
            "country_list": scenario_country_list,
            "price_per_km": scenario_price_per_km,
            "co2_per_km": scenario_co2_per_km,
            "total_cost": scenario_costs,
            "total_co2": scenario_co2,
            "total_cost_per_order": scenario_total_cost_per_order,
            "total_co2_per_order": scenario_total_co2_per_order,
        }
    )
    df_comparison = df_comparison.sort_values(by="total_cost")
    df_comparison = df_comparison.reset_index()

    state.df_comparison = df_comparison


df_comparison = pd.DataFrame(
    {
        "scenario_name": [],
        "optimization_target": [],
        "number_of_warehouses": [],
        "country_list": [],
        "price_per_km": [],
        "co2_per_km": [],
        "total_cost": [],
        "total_co2": [],
        "total_cost_per_order": [],
        "total_co2_per_order": [],
    }
)


with tgb.Page() as total_comparison_page:

    tgb.text("# **All** Scenarios", mode="md")

    tgb.button(
        "Compare all scenarios",
        on_action=refresh_all_scenarios,
        class_name="fullwidth",
    )

    tgb.table("{df_comparison}", rebuild=True)

    tgb.html("hr")

    with tgb.layout("1 1"):
        tgb.chart(
            "{df_comparison}",
            type="bar",
            x="scenario_name",
            y="total_cost",
            title="Scenarios by cost",
            color="#003399",
            rebuild=True,
        )
        tgb.chart(
            "{df_comparison}",
            type="bar",
            x="scenario_name",
            y="total_co2",
            title="Scenarios by CO2e emissions (metric Tons)",
            color="#003399",
            rebuild=True,
        )
    tgb.chart(
        "{df_comparison}",
        mode="markers",
        x="total_cost",
        y="total_co2",
        title="Cost vs CO2e",
        marker={
            "color": "#003399",
        },
        rebuild=True,
    )
