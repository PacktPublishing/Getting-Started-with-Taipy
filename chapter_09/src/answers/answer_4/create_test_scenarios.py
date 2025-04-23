import taipy as tp


def create_and_submit_scenario(id_name, year, scenario_config):
    scenario_name = f"{id_name} - {year}"

    scenario = tp.create_scenario(config=scenario_config, name=scenario_name)
    scenario.selected_year.write(year)
    scenario.id_name.write(id_name)
    if year in [2020, 2021]:
        scenario.tags = [f"year: {year}", f"park: {id_name}", "non-organic"]
    else:
        scenario.tags = [f"year: {year}", f"park: {id_name}", "organic"]
    scenario.submit()
    return scenario


def create_test_scenarios(scenario_config, parks_file="./data/paris_parks.csv"):
    # Bois de Vincennes: 1679
    vincennes = "1679 - Bois De Vincennes"
    for year in range(2020, 2024):
        create_and_submit_scenario(vincennes, year, scenario_config)

    # return a specific Scenario for selection
    return create_and_submit_scenario(vincennes, 2024, scenario_config)
