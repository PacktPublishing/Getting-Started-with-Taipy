def calculate_total_numbers(df_scenario):
    """
    Returns the total price and CO2 emissions for a Scenario (for all warehouses).
    Returns total amounts and total amount per truck order.
    """
    total_cost = df_scenario["scenario_cost"].sum()
    total_co2 = df_scenario["scenario_co2_tons"].sum()

    total_orders = df_scenario["scenario_orders"].sum()
    price_per_order = total_cost / total_orders
    co2_per_order = total_co2 * 1000 / total_orders

    return int(total_cost), int(total_co2), int(price_per_order), int(co2_per_order)
