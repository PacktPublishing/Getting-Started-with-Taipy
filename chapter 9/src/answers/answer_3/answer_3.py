import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb

df_ndvi_summary = pd.DataFrame()


def rank_scenarios(state):
    all_scenarios = tp.get_scenarios()

    scenario_name_list = [scenario.name for scenario in all_scenarios]
    max_ndvi_list = [
        round(float(scenario.tif_image.read().max()), 2) for scenario in all_scenarios
    ]
    avg_ndvi_list = [
        round(float(scenario.tif_image.read().mean()), 2) for scenario in all_scenarios
    ]

    df_summary = pd.DataFrame(
        {
            "scenario_name": scenario_name_list,
            "max_ndvi": max_ndvi_list,
            "average_ndvi": avg_ndvi_list,
        }
    )
    df_summary = df_summary.sort_values(by="average_ndvi")
    state.df_ndvi_summary = df_summary


with tgb.Page() as answer_3_page:
    tgb.text("## **NDVI** Comparison", mode="md")
    tgb.html("hr")

    tgb.button(label="Update Scenarios", on_action=rank_scenarios)

    tgb.table("{df_ndvi_summary}", rebuild=True)
    tgb.chart("{df_ndvi_summary}", type="bar", rebuild=True)
