def calculate_minimum(state):
    # Answer 2:
    selected_cycle = state.selected_scenario.cycle
    scenario_list = tp.get_scenarios(selected_cycle)
    buying_prices = [
        price
        for scenario in scenario_list
        if (price := scenario.selling_price_node.read()) is not None
    ]
    min_price = min(buying_prices) if buying_prices else None
    print(f"Minimum price for {selected_cycle} is {min_price}")

    # You can call this function from update_scenario
