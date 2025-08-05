import time

import taipy as tp
from taipy import Config, Gui
from taipy.core import SubmissionStatus
from taipy.event.event_processor import EventEntityType, EventOperation, EventProcessor
from taipy.gui import builder as tgb
from taipy.gui import notify


def track_events(event, gui):
    print(f"event: {event.entity_id}")
    print(f"operation: {event.operation}")
    print(f"event type: {event.entity_type} - {event.creation_date}")

    scenario = tp.get(event.entity_id)
    input_value = scenario.input_node.read()
    print(f"The input value for the Scenario is: {input_value}")
    if input_value >= 10:
        scenario_tag = "value_over_10"
    else:
        scenario_tag = "value_under_10"
    tp.tag(scenario, scenario_tag)


def notify_add(state, event, gui):
    if event.attribute_value in (SubmissionStatus.BLOCKED, SubmissionStatus.COMPLETED):
        if "add_1_sleep_5" in event.metadata.get(
            "job_triggered_submission_status_changed"
        ):
            with state as s:
                s.middle_number_1 = scenario_1.middle_node.read()
                s.middle_number_2 = scenario_2.middle_node.read()
                notify(s, "w", "Added 1 successfully!")
        elif "add_2_sleep_5" in event.metadata.get(
            "job_triggered_submission_status_changed"
        ):
            with state as s:
                s.output_number_1 = scenario_1.output_node.read()
                s.output_number_2 = scenario_2.output_node.read()
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
    tgb.button("add numbers", on_action=add_numbers)

    with tgb.layout("1 1 1"):
        tgb.text("## SCENARIO", mode="md")
        tgb.text("#### Add 1", mode="md")
        tgb.text("#### Add 2", mode="md")

    tgb.text("### Scenario 1", mode="md")
    with tgb.layout("1 1 1"):
        tgb.number("{number_1}", label="Input number 1", min=0, max=10)
        tgb.text("{middle_number_1}")
        tgb.text("{output_number_1}")

    tgb.text("### Scenario 2", mode="md")
    with tgb.layout("1 1 1"):
        tgb.number("{number_2}", label="Input number 2", min=0, max=10)
        tgb.text("{middle_number_2}")
        tgb.text("{output_number_2}")
    tgb.scenario("{scenario_1}", show_submit=False, show_delete=True)

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
        callback=track_events,
        operation=EventOperation.SUBMISSION,
        entity_type=EventEntityType.SCENARIO,
    )
    event_processor.broadcast_on_event(
        callback=notify_add,
        operation=EventOperation.UPDATE,
        entity_type=EventEntityType.SUBMISSION,
    )
    event_processor.start()

    scenario_1 = tp.create_scenario(scenario_config, name="scenario_1")
    scenario_2 = tp.create_scenario(scenario_config, name="scenario_2")

    # Run to start a server
    gui.run(dark_mode=False, use_reloader=True)
