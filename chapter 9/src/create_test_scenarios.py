import pandas as pd
import taipy as tp


def create_and_submit_scenario(id_name, year, scenario_config, df_parks):
    park_name = df_parks[df_parks["id_name"] == id_name]["id_name"].iloc[0]

    scenario_name = f"{id_name} - {year}"

    scenario = tp.create_scenario(config=scenario_config, name=scenario_name)
    scenario.selected_year.write(year)
    scenario.id_name.write(park_name)
    scenario.tags = [f"year: {year}", f"park: {id_name}"]
    scenario.submit()
    return scenario


def create_test_scenarios(scenario_config, parks_file="./data/paris_parks.csv"):
    df_parks = pd.read_csv(parks_file)
    # Bois de Vincennes: 1679
    vincennes = "1679 - Bois De Vincennes"
    for year in range(2023, 2024):
        create_and_submit_scenario(vincennes, year, scenario_config, df_parks)

    # return a specific Scenario for selection
    return create_and_submit_scenario(vincennes, 2024, scenario_config, df_parks)
