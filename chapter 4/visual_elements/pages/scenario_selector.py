import taipy.gui.builder as tgb
from orchestration import auto_scenario

selected_scenario = auto_scenario


with tgb.Page() as scenario_selector:
    tgb.text("# Scenario selector", mode="md")

    tgb.scenario_selector(
        value="{selected_scenario}",
        show_pins=True,
        show_add_button=False,
    )
