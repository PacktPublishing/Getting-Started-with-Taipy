###############################################
## Move this file to the auto_mpg directory  ##
## And run it with taipy run answer_5.py     ##
###############################################


import taipy.gui.builder as tgb
from orchestration import predicting_scenario, training_scenario
from taipy import Gui

selected_scenario = training_scenario
selected_job = None

prediction_cylinders = 1
prediction_displacement = 50
prediction_horsepower = 40
prediction_weight = 3500
prediction_acceleration = 10
prediction_model_year = 75
prediction_origin = 1

predicting_scenario.cylinders.write(prediction_cylinders)
predicting_scenario.displacement.write(prediction_displacement)
predicting_scenario.horsepower.write(prediction_horsepower)
predicting_scenario.weight.write(prediction_weight)
predicting_scenario.acceleration.write(prediction_acceleration)
predicting_scenario.modelyear.write(prediction_model_year)
predicting_scenario.origin.write(prediction_origin)

predicted_mpg = 0

columns_lov = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model year",
    "origin",
]
selected_columns = columns_lov


show_cylinders = True
show_displacement = True
show_horsepower = True
show_weight = True
show_acceleration = True
show_model_year = True
show_origin = True

predicted_mpg = 0


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


def change_column(state):
    training_scenario.column_subset.write(state.selected_columns)


def update_prediction(state, var_name, value):
    if var_name == "prediction_cylinders":
        predicting_scenario.cylinders.write(state.prediction_cylinders)
    if var_name == "prediction_displacement":
        predicting_scenario.displacement.write(state.prediction_displacement)
    if var_name == "prediction_horsepower":
        predicting_scenario.horsepower.write(state.prediction_horsepower)
    if var_name == "prediction_weight":
        predicting_scenario.weight.write(state.prediction_weight)
    if var_name == "prediction_acceleration":
        predicting_scenario.acceleration.write(state.prediction_acceleration)
    if var_name == "prediction_model_year":
        predicting_scenario.modelyear.write(state.prediction_model_year)
    if var_name == "prediction_origin":
        predicting_scenario.origin.write(state.prediction_origin)


def change_scenario(state, var_name, value):
    state.selected_scenario = value


def update_mpg(state, submission, details):
    if (
        details["submission_status"] == "COMPLETED"
        and details["submittable_entity"] == predicting_scenario
    ):
        state.predicted_mpg = predicting_scenario.predicted_mpg.read()


with tgb.Page() as orchestration_interface:
    tgb.text("# Orchestration Interface", mode="md")

    with tgb.layout("1 1 1 1 1 1 1 1 1 1"):
        tgb.scenario_selector(
            value="{selected_scenario}",
            show_pins=True,
            show_add_button=False,
            on_change=change_scenario,
        )
        tgb.selector(
            value="{selected_columns}",
            lov="{columns_lov}",
            dropdown=True,
            multiple=True,
            on_change=change_column,
        )
        with tgb.part():
            tgb.text("### Cylinders: ", mode="md")
            tgb.slider(
                value="{prediction_cylinders}",
                lov=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                active="{show_cylinders}",
                on_change=update_prediction,
            )  # dataset beween 3 and 8
        with tgb.part():
            tgb.text("### Displacement: ", mode="md")
            tgb.slider(
                value="{prediction_displacement}",
                min=50,
                max=500,
                active="{show_displacement}",
                on_change=update_prediction,
            )  # dataset between 68 and 455
        with tgb.part():
            tgb.text("### Horsepower: ", mode="md")
            tgb.slider(
                value="{prediction_horsepower}",
                min=40,
                max=250,
                active="{show_horsepower}",
                on_change=update_prediction,
            )
            # dataset between 46 and230
        with tgb.part():
            tgb.text("### Weight: ", mode="md")
            tgb.slider(
                value="{prediction_weight}",
                active="{show_weight}",
                min=1500,
                max=5500,
                on_change=update_prediction,
            )  # dataset between 1613 and 5140
        with tgb.part():
            tgb.text("### Acceleration: ", mode="md")
            tgb.slider(
                value="{prediction_acceleration}",
                min=8,
                max=25,
                step=0.1,
                active="{show_acceleration}",
                on_change=update_prediction,
            )  # dataset between 8 and 24.8, decimal
        with tgb.part():
            tgb.text("### Model Year: ", mode="md")
            tgb.selector(
                value="{prediction_model_year}",
                lov=[str(year) for year in range(70, 86)],
                dropdown=True,
                active="{show_model_year}",
                on_change=update_prediction,
            )
        with tgb.part():
            tgb.text("### Origin: ", mode="md")
            tgb.toggle(
                value="{prediction_origin}",
                lov=[1, 2, 3],
                active="{show_origin}",
                on_change=update_prediction,
            )
        tgb.metric(value="{predicted_mpg}", type="none", title="predicted MPG")

    tgb.scenario(
        scenario="{selected_scenario}",
        show_tags=False,
        show_delete=False,
        show_properties=False,
        on_submission_change=update_mpg,
    )

    tgb.job_selector("{selected_job}", show_submitted_id=True)


auto_mpg_gui = Gui(page=orchestration_interface)


auto_mpg_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Data Node examples",
)
