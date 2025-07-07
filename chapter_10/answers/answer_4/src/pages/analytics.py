import pandas as pd
import taipy.gui.builder as tgb

summary = ""


def update_summary(state):
    state.summary = (
        state.selected_scenario.summarized_conversation.read()
        if state.selected_scenario.summarized_conversation.is_valid
        else None
    )


with tgb.Page() as analytics_page:
    tgb.text("## Analyze_conversation", mode="md", class_name="color-primary")

    with tgb.layout("1 4"):
        tgb.scenario_selector(value="{selected_scenario}", show_add_button=False)
        with tgb.part():
            tgb.scenario(
                scenario="{selected_scenario}",
            )
            tgb.data_node(
                data_node="{selected_scenario.key_parameters}",
                show_properties=False,
                show_history=False,
                show_owner=False,
            )
            tgb.html("br")
            tgb.text("### Text summary", mode="md")
            tgb.data_node(
                data_node="{selected_scenario.summarized_conversation}",
                show_properties=False,
                show_history=False,
                show_owner=False,
            )
