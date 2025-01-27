# Add this variable to the page
cycles_table = None


# This callback function creates a table with the minimum price for each Cycle:
def create_cycles_table(state):
    cycle_rows = []
    for cycle in tp.get_cycles():

        scenario_list = tp.get_scenarios(cycle)
        scenarios = []
        buying_prices = []
        for scenario in scenario_list:
            price = scenario.selling_price_node.read()
            if price is not None:
                buying_prices.append(price)
                scenarios.append(scenario)
            min_price = min(buying_prices) if buying_prices else None
            min_price_scenario = (
                scenarios[buying_prices.index(min_price)] if buying_prices else None
            )
            if min_price_scenario:
                tp.set_primary(min_price_scenario)

        table_row = {
            "cycle": cycle.get_label(),
            "min_price_scenario": (
                min_price_scenario.name if min_price_scenario else None
            ),
            "min_buying_price": min_price,
        }

        cycle_rows.append(table_row)

    df_cycles = pd.DataFrame(cycle_rows)
    state.cycles_table = df_cycles


# Add a button and a table element to the Page
tgb.button(label="Create Cycles table", on_action=create_cycles_table)
tgb.table("{cycles_table}", rebuild=True)
