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


def submit_scenario(state):
    auto_scenario.submit()


with tgb.Page() as regular_ui:
    tgb.text("# Regular UI components", mode="md")

    with tgb.layout("1 1"):
        tgb.selector(
            value="{selected_column}",
            lov=columns_lov,
            dropdown=True,
            multiple=True,
            on_change=change_column,
        )

        tgb.button(label="Submit scenario", on_action=submit_scenario)

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.text("## Data before the transformation:", mode="md")
            tgb.text("Using a Pandas DataFrame", mode="md")
            tgb.table("{df_auto}")

        with tgb.part():
            tgb.text("## Data after the transformation:", mode="md")
            tgb.text("Using a Data Node element", mode="md")
            tgb.data_node("{auto_scenario.filtered_auto_df}")
