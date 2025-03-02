import taipy as tp


def create_test_scenarios(scenario):
    for fixed_warehouse in range(1, 11):
        default_scenario = tp.create_scenario(scenario)
        default_scenario.number_of_warehouses.write(fixed_warehouse)
        default_scenario.name = f"Default Scenario - {fixed_warehouse}"
        default_scenario.submit()
