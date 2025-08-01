import datetime as dt

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from configuration.config import scenario_config
from taipy import Gui, Orchestrator

#################
## Variables   ##
#################

markup = 1.0


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


#################
## Callbacks   ##
#################


def change_markup(state):
    state.selected_scenario.markup_node.write(state.markup)
    # Refreshing the value ensures that value updates in the GUI
    state.refresh("selected_scenario")


def update_scenario(state, var_name, value):
    state.selected_scenario = value

    scenario_date = state.selected_scenario.cycle.creation_date
    scenario_cycle_ym = f"{scenario_date.month}-{scenario_date.year}"
    buying_price = get_monthly_price(scenario_cycle_ym)
    state.selected_scenario.buying_price_node.write(buying_price)

    state.markup = state.selected_scenario.markup_node.read()


################
##    PAGE    ##
################


with tgb.Page() as price_app_page:

    tgb.text("# Price app", mode="md")

    with tgb.layout("1 1 1 1"):

        tgb.scenario_selector("{selected_scenario}", on_change=update_scenario)

        with tgb.part():
            tgb.text("## VAT (Global Scope)", mode="md")
            tgb.data_node(
                data_node="{selected_scenario.vat_node}",
                show_properties=False,
            )
        with tgb.part():
            tgb.text("## Buying Price (Cycle Scope)", mode="md")
            tgb.data_node(
                data_node="{selected_scenario.buying_price_node}",
                show_properties=False,
                display_cycles=True,
            )
        with tgb.part():
            tgb.text("## Markup (Scenario Scope)", mode="md")
            tgb.slider("{markup}", step=0.01, min=1, max=2, on_change=change_markup)
            tgb.data_node(
                data_node="{selected_scenario.markup_node}",
                show_properties=False,
            )
    with tgb.layout("1 1"):
        with tgb.part():
            tgb.text("## Run Scenario", mode="md")
            tgb.scenario("{selected_scenario}")
        with tgb.part():
            tgb.text("## Result", mode="md")
            tgb.data_node(
                data_node="{selected_scenario.selling_price_node}",
                show_properties=False,
            )

    tgb.scenario_dag("{scenario_december_1}")


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

    selected_scenario = scenario_december_1

    selected_scenario.markup_node.write(markup)

    scenario_date = selected_scenario.cycle.creation_date
    scenario_cycle_ym = f"{scenario_date.month}-{scenario_date.year}"
    buying_price = get_monthly_price(scenario_cycle_ym)
    selected_scenario.buying_price_node.write(buying_price)

    price_app_gui.run(
        # use_reloader=True,
        dark_mode=False,
        title="Price app",
    )
