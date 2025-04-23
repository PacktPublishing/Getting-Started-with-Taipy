# Add this function to config_comparison.py:


def compare_price_usd(*prices):
    usd_price = [price * 1.2 if price is not None else None for price in prices]
    return usd_price


# You can also use this function to return prices and margins (use the same function)
def compare_values(*values):
    return list(values)  # values is a set


# Add the function to the scenario configuration:

scenario_config = Config.configure_scenario(
    id="pricing_scenario",
    task_configs=[calculate_price_task_config],
    frequency=Frequency.MONTHLY,
    comparators={
        selling_price_node_config.id: [compare_values, compare_price_usd],
        margin_node_config.id: compare_values,
    },
)


###################
##  In main.py   ##
###################

# This is how the callback function could look:


def compare_scenarios(state):
    comparison = tp.compare_scenarios(
        state.selected_scenario_1, state.selected_scenario_2
    )
    margin_values = comparison["margin_node"]["compare_values"]
    selling_prices = comparison["selling_price_node"]["compare_values"]
    selling_prices_usd = comparison["selling_price_node"]["compare_price_usd"]
    df_compared_prices = pd.DataFrame(
        {
            "Scenario": [
                state.selected_scenario_1.name,
                state.selected_scenario_2.name,
            ],
            "Margin": margin_values,
            "Price": selling_prices,
            "Price (USD)": selling_prices_usd,
        }
    )
    state.comparison_table = df_compared_prices
