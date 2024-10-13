import taipy.gui.builder as tgb
from orchestration import predicting_scenario, training_scenario
from taipy.gui import notify

prediction_cylinders = 1
prediction_displacement = 50
prediction_horsepower = 40
prediction_weight = 3500
prediction_acceleration = 10
prediction_model_year = 75
prediction_origin = 1

predicted_mpg = 0


def predict_mpg(state):

    predicting_scenario.cylinders.write(state.prediction_cylinders)
    predicting_scenario.displacement.write(state.prediction_displacement)
    predicting_scenario.horsepower.write(state.prediction_horsepower)
    predicting_scenario.weight.write(state.prediction_weight)
    predicting_scenario.acceleration.write(state.prediction_acceleration)
    predicting_scenario.modelyear.write(state.prediction_model_year)
    predicting_scenario.origin.write(state.prediction_origin)

    predicting_scenario.submit()

    state.predicted_mpg = predicting_scenario.predicted_mpg.read()


with tgb.Page() as make_predictions:
    tgb.text("# Select values for prediction", mode="md")

    with tgb.layout("1 1"):
        with tgb.layout("1 1"):

            tgb.text("### Cylinders: ", mode="md")
            tgb.slider(
                value="{prediction_cylinders}",
                lov=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                active="{show_cylinders}",
            )  # dataset beween 3 and 8

            tgb.text("### Displacement: ", mode="md")
            tgb.slider(
                value="{prediction_displacement}",
                min=50,
                max=500,
                active="{show_displacement}",
            )  # dataset between 68 and 455

            tgb.text("### Horsepower: ", mode="md")
            tgb.slider(
                value="{prediction_horsepower}",
                min=40,
                max=250,
                active="{show_horsepower}",
            )
            # dataset between 46 and230

            tgb.text("### Weight: ", mode="md")
            tgb.slider(
                value="{prediction_weight}", active="{show_weight}", min=1500, max=5500
            )  # dataset between 1613 and 5140

            tgb.text("### Acceleration: ", mode="md")
            tgb.slider(
                value="{prediction_acceleration}",
                min=8,
                max=25,
                step=0.1,
                active="{show_acceleration}",
            )  # dataset between 8 and 24.8, decimal

            tgb.text("### Model Year: ", mode="md")
            tgb.selector(
                value="{prediction_model_year}",
                lov=[str(year) for year in range(70, 86)],
                dropdown=True,
                active="{show_model_year}",
            )

            tgb.text("### Origin: ", mode="md")
            tgb.toggle(
                value="{prediction_origin}", lov=[1, 2, 3], active="{show_origin}"
            )
        with tgb.part():
            tgb.text("## Predict MPG!", mode="md")
            tgb.button(label="Submit", on_action=predict_mpg)

            tgb.metric(value="{predicted_mpg}", type="none", title="predicted MPG")
