"""
IMPORTANT
This file shows how to create consumer events before Taipy 4.1
Since the simplified the process, I modified the code (and the chapter's section).
However, if you wish to use older versions of Taipy, I'll leav this code here for reference
THIS DOES NOT DO ANYTHING ELSE THAN add_1_2.py!!
"""

import time

import taipy as tp
from taipy import Config, Gui
from taipy.core import Status
from taipy.core.notification import (
    CoreEventConsumerBase,
    EventEntityType,
    EventOperation,
    Notifier,
)
from taipy.gui import builder as tgb
from taipy.gui import notify


def notify_first_add(state):
    with state as s:
        s.middle_number_1 = scenario_1.middle_node.read()
        s.middle_number_2 = scenario_2.middle_node.read()
        notify(s, "s", "Added 1 successfully!")


def notify_second_add(state):
    with state as s:
        s.output_number_1 = scenario_1.output_node.read()
        s.output_number_2 = scenario_2.output_node.read()
        notify(s, "i", "Added 2 successfully!")


class SpecificCoreConsumer(CoreEventConsumerBase):
    def __init__(self, gui):
        self.gui = gui
        reg_id, queue = Notifier.register(
            entity_type=EventEntityType.JOB
            # entity_type=EventEntityType.SCENARIO ## If you comment JOB above and select SCENARIO, no updates will show
        )
        super().__init__(reg_id, queue)

    def process_event(self, event):

        # Uncomment this to see all events pop up in terminal:
        # print(event)

        if (
            event.operation == EventOperation.UPDATE
            and event.entity_type == EventEntityType.JOB
            and event.attribute_value == Status.COMPLETED
            and event.metadata.get("task_config_id") == "add_1_sleep_5"
        ):
            self.gui.broadcast_callback(notify_first_add)
        if (
            event.operation == EventOperation.UPDATE
            and event.entity_type == EventEntityType.JOB
            and event.attribute_value == Status.COMPLETED
            and event.metadata.get("task_config_id") == "add_2_sleep_5"
        ):
            self.gui.broadcast_callback(notify_second_add)


def add_2_sleep_5(input):
    print("Adding 2")
    time.sleep(5)

    result = input + 2

    print(f"result is {result}")
    return result


def add_1_sleep_5(input):
    print("Adding 1")
    time.sleep(5)

    result = input + 1

    print(f"result is {result}")
    return result


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
    SpecificCoreConsumer(gui).start()

    scenario_1 = tp.create_scenario(scenario_config)
    scenario_2 = tp.create_scenario(scenario_config)

    # Run to start a server
    gui.run(dark_mode=False, use_reloader=True)
