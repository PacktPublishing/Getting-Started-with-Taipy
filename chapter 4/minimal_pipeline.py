import taipy as tp
from taipy import Config, Orchestrator


def minimal_function():
    print("I'm super minimal!")


minimal_task_config = Config.configure_task("minimal_task", minimal_function)

minimal_scenario_config = Config.configure_scenario(
    "minimal_scenario", task_configs=[minimal_task_config]
)

orchestrator = Orchestrator()
orchestrator.run()

minimal_scenario = tp.create_scenario(minimal_scenario_config)

minimal_scenario.submit()
