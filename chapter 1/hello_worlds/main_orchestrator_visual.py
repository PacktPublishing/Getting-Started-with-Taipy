"""Taipy Core - configuration from TOML file"""

import taipy as tp
from taipy import Config, Orchestrator

Config.load("./taipy-config.toml")

planets = [
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
]

if __name__ == "__main__":

    Orchestrator().run()

    scenario_cfg = Config.scenarios["hello_scenario"]
    planet_scenario = tp.create_scenario(scenario_cfg)
    for planet in planets:

        planet_scenario.input_planet.write(planet)  # Select by id
        planet_scenario.submit()

        print(planet_scenario.hello_from_planet.read())  # Select by id
