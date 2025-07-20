import taipy as tp
import taipy.gui.builder as tgb
from answers.answer_5.answer_5 import create_comp_partial
from pages.compare_ndvi.charts import plot_ndvi_multi_timeseries

figure_ndvi = None


def select_scenarios(state):
    if state.select_park_name_comp:
        with state as s:
            tag_name = f"park: {s.select_park_name_comp}"
            scenarios_to_compare = tp.get_scenarios(tag=tag_name)

            if len(scenarios_to_compare) > 0:
                s.scenario_comp_names = [
                    scenario.name
                    for scenario in scenarios_to_compare
                    if scenario.ndvi_time_series.is_valid
                    and scenario.tiff_image.is_valid
                ]
                s.selected_time_series_list = [
                    scenario.ndvi_time_series.read()
                    for scenario in scenarios_to_compare
                    if scenario.ndvi_time_series.is_valid
                ]
                s.selected_arrays = [
                    scenario.tiff_image.read()
                    for scenario in scenarios_to_compare
                    if scenario.tiff_image.is_valid
                ]
                s.figure_ndvi = plot_ndvi_multi_timeseries(
                    s.selected_time_series_list,
                    s.scenario_comp_names,
                    s.select_park_name_comp,
                )
            create_comp_partial(state)


with tgb.Page() as compare_page:
    tgb.text("## **NDVI** Comparison", mode="md")
    tgb.html("hr")

    tgb.selector(
        "{select_park_name_comp}",
        lov="{scenarios_to_compare}",
        dropdown=True,
        label="Select park to compare",
        on_change=select_scenarios,
        filter=True,
    )

    tgb.chart(figure="{figure_ndvi}")
    tgb.part(partial="{answer_5_partial}")
