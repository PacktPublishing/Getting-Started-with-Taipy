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
    # input_value = scenario.input_node.read()
    # print(f"The result value for the Scenario is: {input_value}")
    # if input_value < 0:
    #     scenario_tag = "LOOSING MONEY"
    # tp.tag(scenario, scenario_tag)


def notify_add(state, event, gui):
    if event.attribute_value in (SubmissionStatus.BLOCKED, SubmissionStatus.COMPLETED):
        if "calculate_real_wage" in event.metadata.get(
            "job_triggered_submission_status_changed"
        ):
            with state as s:
                s.real_wage_10 = scenario_10.real_wage_node.read()
                s.real_wage_20 = scenario_20.real_wage_node.read()
                notify(s, "w", "Calculated wage after tax!")
        elif "calculate_difference" in event.metadata.get(
            "job_triggered_submission_status_changed"
        ):
            with state as s:
                s.leftover_10 = scenario_10.leftover_node.read()
                s.leftover_20 = scenario_20.leftover_node.read()

                if s.leftover_10 < 0 and s.leftover_20 < 0:
                    notify(s, "e", "You have a money problem!")
                elif s.leftover_20 < 0:
                    notify(s, "w", "Be careful!")
                else:
                    notify(s, "s", "You have money left!")


def calculate_real_wage(wage, tax_rate):
    """We add time.sleep to make the function slower!
    We divide te tax rate by 100 because the UI displays it as percentage
    """
    time.sleep(5)
    print("Calculating real wage")
    tax_rate_decimal = tax_rate / 100
    return wage * (1 - tax_rate_decimal)


def calculate_difference(cost_of_life, real_wage):
    """We add time.sleep to make the function slower!"""
    time.sleep(5)
    print(cost_of_life)
    print(real_wage - cost_of_life)
    return real_wage - cost_of_life


def what_is_left(state):
    with state as s:
        scenario_10.wage_node.write(s.wage)
        scenario_20.wage_node.write(s.wage)
        scenario_10.cost_of_life_node.write(s.cost_of_life)
        scenario_20.cost_of_life_node.write(s.cost_of_life)
    scenario_10.submit()
    scenario_20.submit()


with tgb.Page() as add_page:
    tgb.text("# Calculating Money Left", mode="md")

    with tgb.layout("1 1 4"):
        tgb.number("{wage}", label="Input wage", min=0, max=1_000_000)
        tgb.number("{cost_of_life}", label="Input Cost of Life", min=0, max=1_000_000)
        tgb.button("What's left?", on_action=what_is_left, class_name="plain fullwidth")
    with tgb.layout("1 1 1"):
        tgb.text("## SCENARIO", mode="md")
        tgb.text("#### After Tax", mode="md")
        tgb.text("#### Total Left", mode="md")

    tgb.text("### Scenario 10% Tax", mode="md")
    with tgb.layout("1 1 1"):
        tgb.scenario("{scenario_10}", show_submit=False, show_delete=False)
        tgb.text("## {real_wage_10}", mode="md")
        tgb.text("## {leftover_10}", mode="md")

    tgb.text("### Scenario 20% Tax", mode="md")
    with tgb.layout("1 1 1"):
        tgb.scenario("{scenario_20}", show_submit=False, show_delete=False)
        tgb.text("## {real_wage_20}", mode="md")
        tgb.text("## {leftover_20}", mode="md")


if __name__ == "__main__":
    ######################################
    ### Part 1: Variables              ###
    ######################################
    wage = 0
    cost_of_life = 0
    real_wage_10 = 0
    leftover_10 = 0
    real_wage_20 = 0
    leftover_20 = 0
    ######################################
    ### Part 2: Configuration          ###
    ######################################

    # Uncomment to run in parallel!
    # Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

    # Data Nodes
    wage_node_config = Config.configure_data_node("wage_node", default_data=0)
    tax_rate_node_config = Config.configure_data_node("tax_rate_node", default_data=0)
    cost_of_life_node_config = Config.configure_data_node(
        "cost_of_life_node", default_data=0
    )
    real_wage_node_config = Config.configure_data_node("real_wage_node", default_data=0)
    leftover_node_config = Config.configure_data_node("leftover_node", default_data=0)

    # Tasks
    calculate_real_wage_task = Config.configure_task(
        id="calculate_real_wage",
        function=calculate_real_wage,
        input=[wage_node_config, tax_rate_node_config],
        output=real_wage_node_config,
    )
    calculate_difference_task = Config.configure_task(
        id="calculate_difference",
        function=calculate_difference,
        input=[cost_of_life_node_config, real_wage_node_config],
        output=leftover_node_config,
    )

    # Scenario
    scenario_config = Config.configure_scenario(
        id="my_scenario",
        task_configs=[calculate_real_wage_task, calculate_difference_task],
    )
    Config.export("config_seq.toml")

    ######################################
    ### Part 3: Gui() and events       ###
    ######################################
    gui = Gui(page=add_page)

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

    ######################################
    ### Start Scenarios and run it all ###
    ######################################
    tp.Orchestrator().run()
    event_processor.start()

    scenario_10 = tp.create_scenario(scenario_config, name="scenario_10")
    scenario_20 = tp.create_scenario(scenario_config, name="scenario_20")

    scenario_10.tax_rate_node.write(10)
    scenario_20.tax_rate_node.write(20)

    gui.run(dark_mode=False, use_reloader=True)
