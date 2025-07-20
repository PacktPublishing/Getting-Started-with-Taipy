import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

matplotlib.use("Agg")  # IMPORTANT: Use a non-interactive backend to render in a GUI


def clean_arrange_data(df_cities):
    df_cities["population"] = df_cities["population"].fillna(0)
    df_cities = df_cities.fillna("")
    df_cities = df_cities[df_cities["population"] >= 1_000]
    df_cities = df_cities[
        ["city_ascii", "lat", "lng", "country", "iso3", "capital", "population"]
    ]
    df_cities = df_cities.reset_index(drop=True)
    df_cities["rank"] = df_cities.index + 1
    # Add population category bins
    bins = [
        0,
        100_000,
        500_000,
        1_000_000,
        2_000_000,
        3_000_000,
        4_000_000,
        5_000_000,
        10_000_000,
        float("inf"),
    ]
    labels = [
        "<100k",
        "100k-500k",
        "500k-1M",
        "1M-2M",
        "2M-3M",
        "3M-4M",
        "4M-5M",
        "5M-10M",
        "10M+",
    ]
    df_cities["pop_category"] = pd.cut(
        df_cities["population"], bins=bins, labels=labels, right=False
    )
    df_cities["population_decile"] = (
        pd.qcut(df_cities["population"], 10, labels=False) + 1
    )
    return df_cities


def plot_top_10_cities(top_10):
    print("plotting top 10")
    cities = top_10["city_ascii"]
    populations = top_10["population"]
    countries = top_10["country"]

    unique_countries = countries.unique()
    color_map = {
        country: plt.cm.Set3(i / len(unique_countries))
        for i, country in enumerate(unique_countries)
    }
    bar_colors = [color_map[country] for country in countries]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(cities, populations, color=bar_colors)

    for bar, pop in zip(bars, populations):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(pop / 1_000_000)}M",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_title("Top 10 Cities by Population", fontsize=16)
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    ax.set_xticks(range(len(cities)))
    ax.set_xticklabels(cities, rotation=45, ha="right")
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=color_map[c]) for c in unique_countries
    ]
    ax.legend(
        handles,
        unique_countries,
        title="Country",
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
    )

    plt.tight_layout()
    return fig


def make_plotly(top_10):
    print("plotting top 10")
    fig = px.bar(
        top_10,
        x="city_ascii",
        y="population",
        color="country",
        title="Top 10 Cities by Population",
        labels={"city_ascii": "City", "population": "Population"},
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
    )
    return fig


def get_top_10(df_cities):
    top_10 = df_cities.sort_values(by="population", ascending=False).head(10)
    return top_10


def make_map(df_cities):
    print("making map")
    df_cities_simple = df_cities.copy()[["lng", "lat", "city_ascii", "population"]]
    gdf_cities = gpd.GeoDataFrame(
        df_cities_simple,
        geometry=gpd.points_from_xy(df_cities_simple.lng, df_cities_simple.lat),
        crs="EPSG:4326",
    )
    return gdf_cities.__geo_interface__
