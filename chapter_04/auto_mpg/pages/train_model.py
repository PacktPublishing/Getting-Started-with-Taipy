import taipy.gui.builder as tgb
from taipy.gui import notify

mse = 0
r2 = 0


def change_scenario(state, submission, details):
    state.mse = state.training_scenario.mse.read()
    state.r2 = state.training_scenario.r2.read()
    update_showing_selectors(state)

    notify(state, message="The Scenario is done running")


def change_column(state):
    state.training_scenario.column_subset.write(state.selected_columns)


def update_showing_selectors(state):
    # Update the show_values for the make_predictions app (will show variables, or not)
    state.show_cylinders = True if "cylinders" in state.selected_columns else False
    state.show_displacement = (
        True if "displacement" in state.selected_columns else False
    )
    state.show_horsepower = True if "horsepower" in state.selected_columns else False
    state.show_weight = True if "weight" in state.selected_columns else False
    state.show_acceleration = (
        True if "acceleration" in state.selected_columns else False
    )
    state.show_model_year = True if "model year" in state.selected_columns else False
    state.show_origin = True if "origin" in state.selected_columns else False


with tgb.Page() as train_model:
    tgb.text("# Select Dataset subset", mode="md")

    tgb.selector(
        value="{selected_columns}",
        lov="{columns_lov}",
        dropdown=True,
        multiple=True,
        on_change=change_column,
    )
    tgb.scenario(
        scenario="{training_scenario}",
        on_submission_change=change_scenario,
        show_tags=False,
        show_delete=False,
        show_properties=False,
    )
    with tgb.layout("1 1"):
        tgb.metric(value="{mse}", type="none", title="Mean Squared Error (MSE)")
        tgb.metric(value="{r2}", type="none", title="r2 value")

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.text("## Auto-mpg Dataset:", mode="md")
            tgb.table("{training_scenario.auto_data.read()}")

        with tgb.part():
            tgb.text("## Data for training:", mode="md")
            tgb.text("Using a Data Node element", mode="md")
            tgb.data_node("{training_scenario.filtered_auto_df}")
