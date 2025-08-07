import time

import taipy as tp
from taipy import Config, Gui
from taipy.core import SubmissionStatus
from taipy.event.event_processor import EventEntityType, EventOperation, EventProcessor
from taipy.gui import builder as tgb
from taipy.gui import notify


def _print_event_properties(event):
    print(
        f"""------
event: {event.entity_id}
operation: {event.operation}
event type: {event.entity_type} 
event date: {event.creation_date}
event attribute: {event.attribute_name}
event metadata: {event.metadata}
------
"""
    )


def _read_data_node_and_print_stuff(data_node):
    output_value = data_node.read()
    print(f"The input value for the Scenario is: {output_value}")
    print("value_over_5") if output_value >= 5 else print("value_under_5")


def track_output_data_node(event, gui):
    _print_event_properties(event)
    data_node = tp.get(event.entity_id)
    if data_node.config_id == "output_node":
        _read_data_node_and_print_stuff(data_node)


def notify_add(state, event, gui):
    data_node_config_id = event.metadata.get("config_id")
    data_node = tp.get(event.entity_id)
    # get_parents return scenarios in a set, we se next(iter()) to the the value
    scenario = next(iter(data_node.get_parents().get("scenario")))
    with state as s:
        if data_node_config_id == "middle_node":
            if scenario.name == "scenario_1":
                s.middle_number_1 = scenario.middle_node.read()
            elif scenario.name == "scenario_2":
                s.middle_number_2 = scenario.middle_node.read()
            notify(s, "w", "Added 1 successfully!")
        elif data_node_config_id == "output_node":
            if scenario.name == "scenario_1":
                s.output_number_1 = scenario.middle_node.read()
            elif scenario.name == "scenario_2":
                s.output_number_2 = scenario.middle_node.read()
            notify(s, "s", "Added 2 successfully!")


def add_number(input, number):
    time.sleep(5)
    print(f"Adding {number}")
    result = input + number
    print(f"result is {result}")
    return result


def add_1_sleep_5(input):
    return add_number(input, 1)


def add_2_sleep_5(input):
    return add_number(input, 2)


def add_numbers(state):
    with state as s:
        scenario_1.input_node.write(s.number_1)
        scenario_2.input_node.write(s.number_2)
    scenario_1.submit()
    scenario_2.submit()


with tgb.Page() as add_page:
    tgb.text("# Adding numbers", mode="md")
    with tgb.layout("1 1 1 1"):
        tgb.text("## SCENARIO", mode="md")
        tgb.text("## enter number", mode="md")
        tgb.text("#### Add 1", mode="md")
        tgb.text("#### Add 2", mode="md")

    with tgb.layout("1 1 1 1"):
        tgb.text("### Scenario 1", mode="md")
        tgb.number("{number_1}", label="Input number 1", min=0, max=10)
        tgb.text("## {middle_number_1}", mode="md")
        tgb.text("## {output_number_1}", mode="md")

    with tgb.layout("1 1 1 1"):
        tgb.text("### Scenario 2", mode="md")
        tgb.number("{number_2}", label="Input number 2", min=0, max=10)
        tgb.text("## {middle_number_2}", mode="md")
        tgb.text("## {output_number_2}", mode="md")
    tgb.button(
        "Add Numer for BOTH Scenarios",
        on_action=add_numbers,
        class_name="fullwidth plain",
    )

if __name__ == "__main__":

    number_1 = 0
    middle_number_1 = 0
    output_number_1 = 0

    number_2 = 0
    middle_number_2 = 0
    output_number_2 = 0

    # Uncomment to run in parallel!
    # Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

    # Data Nodes
    input_node_config = Config.configure_data_node("input_node", default_data=0)
    middle_node_config = Config.configure_data_node("middle_node", default_data=0)
    output_node_config = Config.configure_data_node("output_node", default_data=0)

    # Tasks
    add_1_sleep_5_task = Config.configure_task(
        id="add_1_sleep_5",
        function=add_1_sleep_5,
        input=input_node_config,
        output=middle_node_config,
    )
    add_2_sleep_5_task = Config.configure_task(
        id="add_2_sleep_5",
        function=add_2_sleep_5,
        input=middle_node_config,
        output=output_node_config,
    )

    # Configuration
    scenario_config = Config.configure_scenario(
        id="my_scenario", task_configs=[add_1_sleep_5_task, add_2_sleep_5_task]
    )
    Config.export("config_seq.toml")

    gui = Gui(page=add_page)
    tp.Orchestrator().run()

    event_processor = EventProcessor(gui)
    event_processor.on_event(
        callback=track_output_data_node,
        operation=EventOperation.UPDATE,
        entity_type=EventEntityType.DATA_NODE,
        attribute_name="edit_in_progress",
    )
    event_processor.broadcast_on_datanode_written(
        callback=notify_add,
    )
    event_processor.start()

    scenario_1 = tp.create_scenario(scenario_config, name="scenario_1")
    scenario_2 = tp.create_scenario(scenario_config, name="scenario_2")

    # Run to start a server
    gui.run(dark_mode=False, use_reloader=True)
