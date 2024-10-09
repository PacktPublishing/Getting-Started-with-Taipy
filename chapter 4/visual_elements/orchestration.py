import taipy as tp
from configuration.config import auto_scenario_config
from taipy import Orchestrator

orchestrator = Orchestrator()
orchestrator.run()


auto_scenario = tp.create_scenario(auto_scenario_config)
