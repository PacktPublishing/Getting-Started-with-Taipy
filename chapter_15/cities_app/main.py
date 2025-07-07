import pandas as pd
from algorithms.algos import *
from taipy import Gui
from taipy.designer import Page


def filter_by_country(state):
    with state as s:
        df_to_filter = s.df_cities.copy()
        filter_to_apply = s.selected_country

        if filter_to_apply == "All":
            df_cities_display = df_to_filter
        elif filter_to_apply == "Capitals":
            df_cities_display = s.df_capitals.copy()
        else:
            df_to_filter = df_to_filter[
                df_to_filter.country == filter_to_apply
            ].reset_index()
            df_cities_display = df_to_filter

    new_cities_to_display = get_top_10(df_cities_display)
    with state as s:
        s.df_cities_display = new_cities_to_display
        s.top_10_fig = plot_top_10_cities(new_cities_to_display)
        s.leaflet = make_map(new_cities_to_display)
        s.selected_cities_pop = new_cities_to_display["population"].sum()
        s.percent_world_cities = 100 * s.selected_cities_pop / s.total_pop


## Callback ##
def on_change(state, var, val):
    if var == "selected_country":
        filter_by_country(state)


if __name__ == "__main__":
    df_cities = clean_arrange_data(pd.read_csv("./data/worldcities.csv"))
    total_pop = df_cities["population"].sum()

    df_cities_display = df_cities.copy()
    df_cities_display = get_top_10(df_cities_display)
    df_capitals = df_cities[df_cities.capital == "primary"].reset_index()

    list_countries = sorted(list(df_cities["country"].unique()))
    list_country_selection = ["All", "Capitals"] + list_countries
    selected_country = "All"

    top_10_fig = plot_top_10_cities(df_cities_display)
    plotly_fig = make_plotly(df_cities_display)
    # Leaflet maps need geojsonformat - we use GeoPandas to transform our data
    leaflet = make_map(df_cities_display)
    selected_cities_pop = df_cities_display["population"].sum()
    percent_world_cities = 100 * selected_cities_pop / total_pop

    page = Page("main.xprjson")
    Gui(page).run(design=True, title="cities app", use_reloader=True)
