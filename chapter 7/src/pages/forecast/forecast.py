import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from algorithms.create_charts import plot_forecast
from configuration.config import forecast_scenario_config
from taipy.gui import notify


def update_scenario(state):
    if state.selected_scenario is not None:
        state.selected_scenario.forecast_target.write(state.forecast_target)
        state.selected_scenario.gender_forecast.write(state.gender_forecast)
        state.selected_scenario.generation_forecast.write(state.generation_forecast)
        state.selected_scenario.product_forecast.write(state.product_forecast)
        state.selected_scenario.number_of_days.write(state.prediction_number_days)
        notify(state, "s", f"{state.selected_scenario.name} has been updated")
    else:
        notify(state, "w", f"A Scenario needs to be selected")
        state.forecast_fig = None


def create_scenario(state):
    if state.scenario_name == "":
        notify(state, "w", "The Scenario needs to have a name")

    else:
        new_scenario = tp.create_scenario(
            forecast_scenario_config, name=state.scenario_name
        )
        new_scenario.forecast_target.write(state.forecast_target)
        new_scenario.gender_forecast.write(state.gender_forecast)
        new_scenario.generation_forecast.write(state.generation_forecast)
        new_scenario.product_forecast.write(state.product_forecast)
        new_scenario.number_of_days.write(state.prediction_number_days)

        state.selected_scenario = new_scenario
        state.scenario_name = ""
        notify(state, "s", "New Scenario created successfully")


def update_chart(state):
    # read these 2 to ensure having the right data:
    df_agg = state.selected_scenario.aggregated_dataframe.read()
    target = state.selected_scenario.forecast_target.read()
    state.forecast_fig = plot_forecast(
        df_agg=df_agg, target=target, forecast_df=state.df_results
    )


def update_summary(state):
    summary_dict = state.selected_scenario.summary.read()
    total_forecast_value = summary_dict["total_forecast"]
    min_forecast_value = summary_dict["total_conf_min"]
    max_forecast_value = summary_dict["total_conf_max"]

    state.total_forecast_value = f"{total_forecast_value:,.2f}"
    state.min_forecast_value = f"{min_forecast_value:,.2f}"
    state.max_forecast_value = f"{max_forecast_value:,.2f}"


def change_scenario(state):
    state.forecast_target = state.selected_scenario.forecast_target.read()
    state.gender_forecast = state.selected_scenario.gender_forecast.read()
    state.generation_forecast = state.selected_scenario.generation_forecast.read()
    state.product_forecast = state.selected_scenario.product_forecast.read()
    state.prediction_number_days = state.selected_scenario.number_of_days.read()

    # Scenario part:
    state.selected_scenario_name = state.selected_scenario.name

    # The Scenario can be create but never run before, therefore:
    if state.selected_scenario.forecast_df.is_ready_for_reading:
        state.df_results = state.selected_scenario.forecast_df.read()
        update_chart(state)
        update_summary(state)
    else:
        state.df_results = pd.DataFrame(
            columns=["date", "forecast", "conf_min", "conf_max"]
        )  # initial value
        state.forecast_fig = None
        state.total_forecast_value = 0
        state.min_forecast_value = 0
        state.max_forecast_value = 0

    notify(state, "i", f"New Scenario selected: {state.selected_scenario.name}")


def update_results(state, submission, details):
    if details["submission_status"] == "COMPLETED":
        state.show_predictions = True
        state.df_results = state.selected_scenario.forecast_df.read()
        state.selected_scenario_name = state.selected_scenario.name

        update_summary(state)
        update_chart(state)


with tgb.Page() as forecast_page:
    tgb.text("## Forecast Sales", mode="md", class_name="color-primary")
    tgb.text(
        "Predict sales (usd) or items for all segments, or filter by product and/or customer type. Keep in mind that excessive filtering may lead to insufficient data and less accurate predictions.",
        mode="md",
        class_name="color-secondary",
    )
    with tgb.layout("1 1 1 1"):
        tgb.toggle(
            value="{forecast_target}",
            lov=["sales", "items"],
            label="Select values to predict",
        )
        tgb.selector(
            value="{gender_forecast}",
            lov=["All", "F", "M"],
            label="Select gender for forecast",
            dropdown=True,
        )
        tgb.selector(
            value="{generation_forecast}",
            lov=[
                "All",
                "Gen X",
                "Boomers",
                "Millenial",
            ],  # Not enough Silent Gen individuals for forecast
            label="Select gender for forecast",
            dropdown=True,
        )
        tgb.selector(
            value="{product_forecast}",
            lov=["All", "Road", "Mountain", "Touring"],
            label="Select product for forecast",
            dropdown=True,
        )
        tgb.input(value="{scenario_name}", label="Scenario Name")
        tgb.number("{prediction_number_days}", label="number of days", min=1, max=365)
        tgb.button(label="Create Scenario", on_action=create_scenario)
        tgb.button(
            label="Update Scenario values",
            on_action=update_scenario,
            class_name="color_secondary",
        )

    # Scenario selectors:
    with tgb.layout("1 3"):
        tgb.scenario_selector(
            value="{selected_scenario}",
            show_add_button=False,
            on_change=change_scenario,
        )
        tgb.scenario(
            scenario="{selected_scenario}", on_submission_change=update_results
        )

    # Forecast results
    tgb.text("## Forecast results", mode="md", class_name="color-primary")
    tgb.text("#### Results for Scenario: {selected_scenario_name}", mode="md")
    with tgb.layout("1 1 1"):
        with tgb.part("card"):
            tgb.text(
                "### Forecast Value for period:",
                mode="md",
                class_name="color-secondary",
            )
            tgb.text(
                "#### {total_forecast_value}", mode="md", class_name="color-primary"
            )
        with tgb.part("card"):
            tgb.text(
                "### Max Value for period:", mode="md", class_name="color-secondary"
            )
            tgb.text("#### {max_forecast_value}", mode="md", class_name="color-primary")
        with tgb.part("card"):
            tgb.text(
                "### Min Value for period:", mode="md", class_name="color-secondary"
            )
            tgb.text("#### {min_forecast_value}", mode="md", class_name="color-primary")

    with tgb.layout("2 1"):
        tgb.chart(figure="{forecast_fig}")
        tgb.table(data="{df_results}", downloadable=True, rebuild=True)

    # tgb.scenario_dag(scenario="{selected_scenario}")
