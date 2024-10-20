import taipy.gui.builder as tgb
from taipy.gui import notify


def change_scenario(state, submission, details):
    notify(state, message="The Scenario is done running")


with tgb.Page() as scenario_element:
    tgb.text("# Scenario element", mode="md")

    tgb.scenario(
        scenario="{auto_scenario}",
        on_submission_change=change_scenario,
        show_sequences=False,
        show_tags=False,
    )
