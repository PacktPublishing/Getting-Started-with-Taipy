import taipy as tp
from taipy import Config, Orchestrator

minimal_data_node_config = Config.configure_data_node(id="minimal_data_node")

minimal_scenario_config = Config.configure_scenario(
    "minimal_scenario", additional_data_node_configs=minimal_data_node_config
)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()

    minimal_message = "I'm a minimal message!"

    minimal_scenario = tp.create_scenario(minimal_scenario_config)
    minimal_scenario.minimal_data_node.write(minimal_message)

    minimal_scenario.submit()
    print(minimal_scenario.minimal_data_node.read())
