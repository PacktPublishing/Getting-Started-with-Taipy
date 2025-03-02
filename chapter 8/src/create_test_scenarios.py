import taipy as tp


def create_test_scenarios(scenario):
    # First Scenario
    test_scenario1 = tp.create_scenario(scenario)
    test_scenario1.number_of_warehouses.write(5)
    test_scenario1.name = "5 warehouse Scenario"
    test_scenario1.submit()

    # Second Scenario
    test_scenario2 = tp.create_scenario(scenario)
    test_scenario2.optimization_target.write("co2")
    test_scenario2.name = "CO2 default"
    test_scenario2.submit()

    # Third Scenario
    test_scenario3 = tp.create_scenario(scenario)
    test_scenario3.number_of_warehouses.write(2)
    test_scenario3.country_list.write(["Portugal", "Poland"])
    test_scenario3.name = "Extreme Countries Scenario"
    test_scenario3.submit()
