import datetime as dt

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from configuration.config_comparison import scenario_config
from taipy import Gui, Orchestrator

#################
## Variables   ##
#################

markup_1 = 1.0
markup_2 = 1.0
comparison_table = pd.DataFrame(columns=["Scenario", "Price"])

#################
## functions   ##
#################


def get_monthly_price(scenario_ym, price_file="./data/buying_prices.csv"):
    df_prices = pd.read_csv(price_file)
    try:
        price = df_prices.loc[df_prices["month"] == scenario_ym, "price"].iloc[0]
        return price
    except:
        print("no data for this period")
        return 0


def write_buying_price(selected_scenario):
    scenario_date = selected_scenario.cycle.creation_date
    scenario_cycle_ym = f"{scenario_date.month}-{scenario_date.year}"
    buying_price = get_monthly_price(scenario_cycle_ym)
    selected_scenario.buying_price_node.write(buying_price)


#################
## Callbacks   ##
#################


def change_markup(state, var_name, value):
    if var_name == "markup_1":
        state.selected_scenario_1.markup_node.write(value)
    else:
        state.selected_scenario_2.markup_node.write(value)


def update_scenario(state, var_name, value):

    write_buying_price(value)

    if var_name == "selected_scenario_1":
        state.markup_1 = value.markup_node.read()
    else:
        state.markup_2 = value.markup_node.read()


def compare_scenarios(state):
    comparison = tp.compare_scenarios(
        state.selected_scenario_1, state.selected_scenario_2
    )
    selling_prices = comparison["selling_price_node"]["compare_price"]
    df_compared_prices = pd.DataFrame(
        {
            "Scenario": [
                state.selected_scenario_1.name,
                state.selected_scenario_2.name,
            ],
            "Price": selling_prices,
        }
    )
    state.comparison_table = df_compared_prices


################
##    PAGE    ##
################


with tgb.Page() as price_app_page:

    tgb.text("# Price App - Compare", mode="md")

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.text("## Compare Scenario 1", mode="md")
            tgb.scenario_selector("{selected_scenario_1}", on_change=update_scenario)
            tgb.slider("{markup_1}", step=0.01, min=1, max=2, on_change=change_markup)
            tgb.scenario("{selected_scenario_1}")

        with tgb.part():
            tgb.text("## Compare Scenario 2", mode="md")
            tgb.scenario_selector("{selected_scenario_2}", on_change=update_scenario)
            tgb.slider("{markup_2}", step=0.01, min=1, max=2, on_change=change_markup)
            tgb.scenario("{selected_scenario_2}")

    tgb.button(label="Compare Scenarios", on_action=compare_scenarios)
    tgb.table("{comparison_table}", rebuild=True)


################
##    Gui     ##
################

price_app_gui = Gui(
    page=price_app_page,
)

################
##  run app   ##
################

if __name__ == "__main__":

    Orchestrator().run()

    scenario_december_1 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2024, 12, 1),
        name="Scenario 1 - December",
    )
    scenario_december_2 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2024, 12, 1),
        name="Scenario 2 - December",
    )
    scenario_january_1 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2025, 1, 1),
        name="Scenario 1 - January",
    )
    scenario_january_2 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2025, 1, 1),
        name="Scenario 2 - January",
    )

    selected_scenario_1 = scenario_december_1
    selected_scenario_2 = scenario_december_2

    write_buying_price(selected_scenario_1)
    write_buying_price(selected_scenario_2)

    price_app_gui.run(
        # use_reloader=True,
        dark_mode=False,
        title="Price app",
    )
