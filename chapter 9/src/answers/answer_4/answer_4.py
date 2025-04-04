import pandas as pd
import plotly.express as px
import taipy as tp
import taipy.gui.builder as tgb

df_ndvi_summary = pd.DataFrame()
ndvi_organic = None


def get_scenario_stats(scenarios):
    names = [scenario.name for scenario in scenarios]
    max_ndvi = [
        round(float(scenario.tif_image.read().max()), 2) for scenario in scenarios
    ]
    avg_ndvi = [
        round(float(scenario.tif_image.read().mean()), 2) for scenario in scenarios
    ]
    return names, max_ndvi, avg_ndvi


def compare_organic(state):
    organic_scenarios = tp.get_scenarios(tag="organic")
    non_organic_scenarios = tp.get_scenarios(tag="non-organic")

    organic_names, max_organic, avg_organic = get_scenario_stats(organic_scenarios)
    non_organic_names, max_non_organic, avg_non_organic = get_scenario_stats(
        non_organic_scenarios
    )

    df_summary_organic = pd.DataFrame(
        {
            "name": organic_names,
            "max_ndvi": max_organic,
            "avg_ndvi": avg_organic,
            "type": "organic",
        }
    )

    df_summary_non_organic = pd.DataFrame(
        {
            "name": non_organic_names,
            "max_ndvi": max_non_organic,
            "avg_ndvi": avg_non_organic,
            "type": "non-organic",
        }
    )

    state.df_ndvi_summary = pd.concat([df_summary_organic, df_summary_non_organic])


def plot_avg_ndvi(df):
    fig = px.violin(
        df,
        x="type",
        y="avg_ndvi",
        box=True,  # Show inner boxplot
        points="all",
        hover_data=["name"],
        title="Average NDVI Density Distribution",
    )
    return fig


def plot_max_ndvi(df):
    fig = px.violin(
        df,
        x="type",
        y="max_ndvi",
        box=True,
        points="all",
        hover_data=["name"],
        title="Max NDVI Density Distribution",
    )
    return fig


with tgb.Page() as answer_4_page:
    tgb.text("## **Organic** Comparison", mode="md")
    tgb.html("hr")
    tgb.button(label="Compare Growing Tyes", on_action=compare_organic)

    with tgb.layout("1 1"):
        tgb.chart(figure=lambda df_ndvi_summary: plot_max_ndvi(df_ndvi_summary))
        tgb.chart(figure=lambda df_ndvi_summary: plot_avg_ndvi(df_ndvi_summary))
