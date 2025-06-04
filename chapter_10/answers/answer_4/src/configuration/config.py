from algorithms.scenario_functions import (
    ask_for_summary,
    build_prompt_from_conversation,
    extract_key_parameters,
    load_conversation,
)

from taipy import Config

#####################
##  Configuration  ##
#####################

### Data Nodes ###
history_data_node_config = Config.configure_data_node(
    id="conversation_history",
)
conversation_data_node_config = Config.configure_data_node(
    id="conversation_dict",
)
key_parameters_data_node_config = Config.configure_data_node(id="key_parameters")
conversation_to_summarize_data_node_config = Config.configure_data_node(
    id="conversation_to_summarize"
)
summary_data_node_config = Config.configure_data_node(id="summarized_conversation")

### tasks###
get_conversation_task_config = Config.configure_task(
    id="get_conversation",
    function=load_conversation,
    input=history_data_node_config,
    output=conversation_data_node_config,
)
get_key_parameters_task_config = Config.configure_task(
    id="get_key_parameters",
    function=extract_key_parameters,
    input=conversation_data_node_config,
    output=key_parameters_data_node_config,
)
build_summary_prompt_task_config = Config.configure_task(
    id="build_summary_prompt",
    function=build_prompt_from_conversation,
    input=conversation_data_node_config,
    output=conversation_to_summarize_data_node_config,
)
summarize_task_config = Config.configure_task(
    id="summarize",
    function=ask_for_summary,
    input=conversation_to_summarize_data_node_config,
    output=summary_data_node_config,
    skippable=True,
)

### Scenario ####
conversation_scenario = Config.configure_scenario(
    id="conversation_scenario",
    task_configs=[
        get_conversation_task_config,
        get_key_parameters_task_config,
        build_summary_prompt_task_config,
        summarize_task_config,
    ],
)

Config.export("config.toml")
