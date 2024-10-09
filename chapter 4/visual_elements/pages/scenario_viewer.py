import taipy.gui.builder as tgb
from orchestration import auto_scenario

df_auto = auto_scenario.auto_data.read()

columns_lov = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model year",
    "origin",
    "car name",
]
selected_column = columns_lov


def change_column(state):
    auto_scenario.column_subset.write(state.selected_column)


with tgb.Page() as scenario_viewer:
    tgb.text("# Scenario viewer", mode="md")

    tgb.scenario(scenario="{auto_scenario}")
