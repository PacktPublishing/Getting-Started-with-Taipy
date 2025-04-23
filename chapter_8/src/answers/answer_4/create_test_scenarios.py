import datetime as dt

import taipy as tp

kilometer_prices = {
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


def create_test_scenarios(scenario):
    # First Scenario
    test_scenario1 = tp.create_scenario(
        scenario,
        creation_date=dt.datetime(2025, 2, 7),
    )
    test_scenario1.number_of_warehouses.write(5)
    test_scenario1.price_per_km.write(4)
    test_scenario1.name = "5 warehouses Feb"
    test_scenario1.submit()

    # Second Scenario
    test_scenario2 = tp.create_scenario(
        scenario,
        creation_date=dt.datetime(2025, 3, 7),
    )
    test_scenario2.number_of_warehouses.write(5)
    test_scenario2.price_per_km.write(4.08)
    test_scenario2.name = "5 warehouses Mar"
    test_scenario2.submit()

    # Third Scenario
    test_scenario3 = tp.create_scenario(
        scenario,
        creation_date=dt.datetime(2025, 12, 7),
    )
    test_scenario3.number_of_warehouses.write(5)
    test_scenario3.price_per_km.write(4.5)
    test_scenario3.name = "5 warehouses Dec"
    test_scenario3.submit()
