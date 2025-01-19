import time

import taipy as tp
from taipy import Config, Gui
from taipy.core.config import Config


def add_2_sleep_5(input):
    print("Adding 2")
    time.sleep(5)
    
    result = input + 2
    
    print(f"result is {result}")
    return result

def add_1_sleep_5(input):
    print("Adding 1")
    time.sleep(5)
    
    result = input + 2
    
    print(f"result is {result}")
    return result

def on_init(state):
    scenario_1 = tp.create_scenario(scenario_config)
    scenario_2 = tp.create_scenario(scenario_config)
    scenario_1.submit()
    scenario_2.submit()

if __name__=="__main__":

    # Uncomment to run in parallel!
    # Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

    # Data Nodes
    input_node_config = Config.configure_data_node("input_node", default_data=1)
    middle_node_config = Config.configure_data_node("middle_node", default_data=1)
    output_node_config = Config.configure_data_node("output_node", default_data=1)


    # Tasks
    add_1_sleep_5_task = Config.configure_task(id="add_1_sleep_5",
                                        function=add_1_sleep_5,
                                        input=input_node_config, output=middle_node_config)
    add_2_sleep_5_task = Config.configure_task(id="add_2_sleep_5",
                                        function=add_2_sleep_5,
                                        input=middle_node_config, output=output_node_config)

    # Configuration
    scenario_config = Config.configure_scenario(id="my_scenario",
                                            task_configs=[add_1_sleep_5_task, add_2_sleep_5_task])
    Config.export("config_seq.toml")

    tp.Orchestrator().run()
    
    # Run to start a server
    Gui(page=" ").run()