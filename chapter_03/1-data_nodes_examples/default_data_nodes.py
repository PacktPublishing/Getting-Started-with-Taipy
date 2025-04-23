import taipy as tp
from taipy import Config, Orchestrator, Scope

## Input with default node ##
country_node_config = Config.configure_data_node(
    id="input_country", scope=Scope.GLOBAL, additional_argument="A cool country!"
)

## Access configuration object properties
print(f"The id of the config object is: {country_node_config.id}")
print(f"We also added a custom argument: {country_node_config.additional_argument}")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
    country_data_node_1 = tp.create_global_data_node(country_node_config)
    country_data_node_2 = tp.create_global_data_node(country_node_config)

    country_data_node_1.write("Senegal")
    senegal = country_data_node_1.read()
    country_data_node_2.write("Nigeria")
    nigeria = country_data_node_2.read()
    print(senegal)
    print(nigeria)
    country_data_node_1.write(12.6)
    not_senegal = country_data_node_1.read()
    print(not_senegal)

    orchestrator.stop()
