import numpy as np
import taipy as tp
import taipy.gui.builder as tgb
from configuration.config import ndvi_scenario_config
from pages.calculate_ndvi.charts import plot_box, plot_ndvi, plot_ndvi_timeseries
from taipy.gui import invoke_long_callback, notify
from update_callbacks import update_compare_selector

# Display variable

show_scenario_selectors = True


def update_selectors(state):
    with state as s:
        s.selected_year = s.selected_scenario.selected_year.read()
        s.selected_park_ndvi = s.selected_scenario.name


def change_scenario(state):
    print("changing Scenario")
    with state as s:
        s.selected_np_tiff = s.selected_scenario.tiff_image.read()
        s.selected_df_time_series = s.selected_scenario.ndvi_time_series.read()
        s.selected_scenario_name = s.selected_scenario.name
        update_selectors(state)
        notify(s, "i", "Changed Scenario")


def submit_scenario(scenario):
    scenario.submit()
    return scenario


def is_multiple_of_60(number):
    return number % 60 == 0


def update_status(state, status, scenario):
    if isinstance(status, bool):
        if status:
            with state as s:
                s.selected_scenario = scenario
                change_scenario(s)
                s.show_scenario_selectors = True
                update_compare_selector(s)  # Update the selector for the compare page!
                notify(s, "s", f"New Scenario created - {scenario.name}!")
        else:
            notify(state, "e", "Scenario Generation Failed")
    else:
        if is_multiple_of_60(status):
            notify(state, "i", f"{status/60} min... Calculations running")


def create_scenario(state):
    with state as s:
        id = int(s.selected_park_ndvi.split("-")[0].strip())
        park_name = s.selected_park_ndvi.split("-", 1)[1].strip()
        scenario_name = f"{s.selected_park_ndvi} - {s.selected_year}"

        existing_scenarios = [scenario.name for scenario in tp.get_scenarios()]
        if scenario_name in existing_scenarios:
            print("Scenario already exists!")
            notify(s, "w", f"Scenario {scenario_name} already exists")
        else:
            s.show_scenario_selectors = False
            new_scenario = tp.create_scenario(config=ndvi_scenario_config)
            new_scenario.selected_year.write(s.selected_year)
            new_scenario.park_name.write(park_name)
            new_scenario.park_id.write(id)
            new_scenario.name = scenario_name

            new_scenario.tags = [f"year: {s.selected_year}", f"park: {park_name}"]
            invoke_long_callback(
                s, submit_scenario, [new_scenario], update_status, [], 2000
            )


with tgb.Page() as ndvi_page:
    tgb.text("## **NDVI** Calculation", mode="md")
    tgb.html("hr")

    with tgb.layout("1 4", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.scenario_selector(
                "{selected_scenario}", on_change=change_scenario, show_add_button=False
            )

        with tgb.part("main content"):

            with tgb.part():
                with tgb.layout("1 1"):
                    tgb.selector(
                        value="{selected_year}",
                        lov=[2020, 2021, 2022, 2023, 2024],
                        label="Select year",
                        dropdown=True,
                        active="{show_scenario_selectors}",
                    )
                    tgb.selector(
                        value="{selected_park_ndvi}",
                        lov="{id_name_list}",
                        label="Select park",
                        dropdown=True,
                        filter=True,
                        active="{show_scenario_selectors}",
                    )
                tgb.button(
                    "Create_Scenario",
                    on_action=create_scenario,
                    class_name="fullwidth",
                    active="{show_scenario_selectors}",
                )
            tgb.html("hr")
            tgb.text("### NDVI values", mode="md")
            with tgb.layout("1 1 1"):
                tgb.metric(
                    value="{float(selected_np_tiff.max())}",
                    type="linear",
                    min=-1,
                    max=1,
                    title="Max NDVI for area and season",
                    hover_text="Maximum NDVI value for selected aread and given year.",
                    color_map={
                        -0.2: "#F44336",
                        0: "#FFC107",
                        0.5: "#8BC34A",
                    },
                    bar_color="#12b049",
                )
                tgb.metric(
                    value="{float(selected_np_tiff.mean())}",
                    type="linear",
                    min=-1,
                    max=1,
                    title="Average NDVI for area and season",
                    hover_text="Average NDVI value for selected aread and given year.",
                    color_map={
                        -0.2: "#F44336",
                        0: "#FFC107",
                        0.5: "#8BC34A",
                    },
                    bar_color="#12b049",
                )
                tgb.metric(
                    value="{np.std(selected_np_tiff)}",
                    type=None,
                    title="Standard Deviation",
                )

            with tgb.layout("1 1"):

                tgb.chart(
                    figure=lambda selected_np_tiff, selected_scenario_name: plot_ndvi(
                        selected_np_tiff, selected_scenario_name
                    )
                )
                tgb.chart(
                    figure=lambda selected_np_tiff, selected_scenario_name: plot_box(
                        selected_np_tiff, selected_scenario_name
                    )
                )
            tgb.chart(
                figure=lambda selected_df_time_series, selected_scenario_name: plot_ndvi_timeseries(
                    selected_df_time_series, selected_scenario_name
                )
            )
