import taipy as tp
from configuration.config import conversation_scenario

### Make a function to create Scenarios ###
### We can call this function as we start a new conversation, and on_init ###


def create_history_scenario(file):
    all_scenarios = tp.get_scenarios()
    all_scenarios_names = [scenario.name for scenario in all_scenarios]

    scenario_name = file.replace(".ndjson", "").replace("./history/", "")
    if scenario_name not in all_scenarios_names:
        scenario = tp.create_scenario(conversation_scenario, name=scenario_name)
        scenario.conversation_history.write(scenario_name)
