import taipy.gui.builder as tgb
from taipy.gui import notify


def notify_change(state, var_name, value):
    notify(state, message=f"Selected Scenario: {state.selected_scenario}")


def notify_creation(state, id, payload):
    notify(state, message=f"Created new Scenario: {payload['label']}")


with tgb.Page() as scenario_selector:
    tgb.text("# Scenario selector", mode="md")

    tgb.scenario_selector(
        value="{selected_scenario}",
        show_pins=True,
        on_change=notify_change,
        on_creation=notify_creation,
    )
