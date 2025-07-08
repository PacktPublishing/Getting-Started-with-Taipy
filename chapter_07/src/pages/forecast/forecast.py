import pandas as pd
from algorithms.create_charts import plot_forecast
from configuration.config import forecast_scenario_config

import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import notify


def write_into_scenario(scenario, state):
    with state as s:
        scenario.forecast_target.write(s.forecast_target)
        scenario.gender_forecast.write(s.gender_forecast)
        scenario.generation_forecast.write(s.generation_forecast)
        scenario.product_forecast.write(s.product_forecast)
        scenario.number_of_days.write(
            int(s.prediction_number_days)
        )  # The `number` visual element outputs floats, `periods` must be int.


def update_scenario(state):
    with state as s:
        if s.selected_scenario is not None:
            write_into_scenario(s.selected_scenario, s)
            notify(s, "s", f"{s.selected_scenario.name} has been updated")
        else:
            notify(s, "w", "A Scenario needs to be selected")
            s.forecast_fig = None


def create_scenario(state):
    with state as s:
        if s.scenario_name == "":
            notify(s, "w", "The Scenario needs to have a name")
        else:
            new_scenario = tp.create_scenario(
                forecast_scenario_config, name=s.scenario_name
            )
            write_into_scenario(new_scenario, s)
            s.selected_scenario = new_scenario
            s.scenario_name = ""
            notify(s, "s", "New Scenario created successfully")


def update_chart(state):
    with state as s:
        # read these 2 to ensure having the right data:
        df_agg = s.selected_scenario.aggregated_dataframe.read()
        target = s.selected_scenario.forecast_target.read()
        state.forecast_fig = plot_forecast(
            df_agg=df_agg, target=target, forecast_df=s.df_results
        )


def update_summary(state):
    with state as s:
        summary_dict = s.selected_scenario.summary.read()
        total_forecast_value = summary_dict["total_forecast"]
        min_forecast_value = summary_dict["total_conf_min"]
        max_forecast_value = summary_dict["total_conf_max"]

        s.total_forecast_value = f"{total_forecast_value:,.2f}"
        s.min_forecast_value = f"{min_forecast_value:,.2f}"
        s.max_forecast_value = f"{max_forecast_value:,.2f}"


def change_scenario(state):
    with state as s:
        s.forecast_target = s.selected_scenario.forecast_target.read()
        s.gender_forecast = s.selected_scenario.gender_forecast.read()
        s.generation_forecast = s.selected_scenario.generation_forecast.read()
        s.product_forecast = s.selected_scenario.product_forecast.read()
        s.prediction_number_days = s.selected_scenario.number_of_days.read()

    # Scenario part:
    with state as s:
        s.selected_scenario_name = s.selected_scenario.name

        # The Scenario can be create but never run before, therefore:
        if s.selected_scenario.forecast_df.is_ready_for_reading:
            s.df_results = s.selected_scenario.forecast_df.read()
            update_chart(s)
            update_summary(s)
        else:
            s.df_results = pd.DataFrame(
                columns=["date", "forecast", "conf_min", "conf_max"]
            )  # initial value
            s.forecast_fig = None
            s.total_forecast_value = 0
            s.min_forecast_value = 0
            s.max_forecast_value = 0

        notify(s, "i", f"New Scenario selected: {state.selected_scenario.name}")


def update_results(state, submission, details):

    if details["submission_status"] == "COMPLETED":
        with state as s:
            s.show_predictions = True
            s.df_results = s.selected_scenario.forecast_df.read()
            s.selected_scenario_name = s.selected_scenario.name

            update_summary(s)
            update_chart(s)


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
            label="Select generation for forecast",
            dropdown=True,
        )
        tgb.selector(
            value="{product_forecast}",
            lov=["All", "Road", "Mountain", "Touring"],
            label="Select product for forecast",
            dropdown=True,
        )
        tgb.input(
            value="{scenario_name}", label="Scenario Name"
        )  # Not sure why we are not using Scenario Selector here
        tgb.number("{prediction_number_days}", label="Number of days", min=1, max=365)
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
            scenario="{selected_scenario}",
            on_submission_change=update_results,
            show_config=True,
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
