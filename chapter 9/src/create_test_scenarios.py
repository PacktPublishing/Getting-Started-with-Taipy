import taipy as tp


def create_test_scenarios(scenario):
    # First Scenario
    test_scenario1 = tp.create_scenario(config=scenario)
    test_scenario1.selected_year.write(2024)
    test_scenario1.park_name.write("Bois De Vincennes")
    test_scenario1.park_id.write(1679)  # Bois de Vincennes id
    test_scenario1.name = "Bois De Vincennes - 2024"
    test_scenario1.tags = ["year: 2024", "park: Bois De Vincennes", "non-organic"]
    test_scenario1.submit()
    # Second Scenario
    test_scenario2 = tp.create_scenario(scenario)
    test_scenario2.selected_year.write(2023)
    test_scenario2.park_name.write("Bois De Vincennes")
    test_scenario2.park_id.write(1679)  # Bois de Vincennes id
    test_scenario2.name = "Bois De Vincennes - 2023"
    test_scenario2.tags = ["year: 2023", "park: Bois De Vincennes", "organic"]
    test_scenario2.submit()

    # Third Scenario
    test_scenario3 = tp.create_scenario(scenario)
    test_scenario3.selected_year.write(2022)
    test_scenario3.park_name.write("Bois De Vincennes")
    test_scenario3.park_id.write(1679)  # Bois de Vincennes id
    test_scenario3.name = "Bois De Vincennes - 2022"
    test_scenario3.tags = ["year: 2022", "park: Bois De Vincennes", "organic"]
    test_scenario3.submit()
    return test_scenario1
