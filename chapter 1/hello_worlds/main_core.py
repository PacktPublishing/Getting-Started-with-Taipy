"""Taipy Core - configuration from Python API"""

import taipy as tp
from taipy import Config, Core


def say_hello(planet: str):
    return f"Hello {planet}!"


planet_data_node_cfg = Config.configure_data_node(id="input_planet")
hello_data_node_cfg = Config.configure_data_node(id="hello_from_planet")

say_hello_task_cfg = Config.configure_task(
    "build_msg", say_hello, planet_data_node_cfg, hello_data_node_cfg
)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[say_hello_task_cfg])


Core().run()

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
planet_scenario = tp.create_scenario(scenario_cfg)
for planet in planets:

    planet_scenario.input_planet.write(planet)  # Select by id
    planet_scenario.submit()

    print(planet_scenario.hello_from_planet.read())  # Select by id
