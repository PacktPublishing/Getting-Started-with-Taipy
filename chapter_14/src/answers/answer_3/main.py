import geopandas as gpd
import taipy.gui.builder as tgb
from algorithms.folium_map import FoliumMap, expose_folium_map
from algorithms.js_chart import JsChartClass, expose_js_chart
from algorithms.pydeck_map import DeckMap, expose_deck_map  # Add this for question 3
from pages.dynamic_chart import dynamic_chart_page
from pages.general_info import general_info
from pages.parishes import parishes_page
from taipy.gui import Gui

with tgb.Page() as root:
    tgb.part(page="./iframes/andorra_weather.html", height="55px")
    tgb.text("# Andorra App", mode="md", class_name="color-primary")
    #### ANSWER 3: Add a Pydeck map - you can place this in a better place!!
    tgb.part(content="{DeckMap(gdf_parish_info)}", height="800px")

    tgb.navbar()
    tgb.content()

    with tgb.expandable("Folium Resources", expanded=False):
        with tgb.layout("2 1"):
            tgb.part(
                page="https://python-visualization.github.io/folium/latest/",
                height="350px",
            )
            tgb.part(page="./iframes/yt_video.html", height="350px")

pages = {
    "/": root,
    "general_info": general_info,
    "parishes": parishes_page,
    "dynamic_charts": dynamic_chart_page,
}

if __name__ == "__main__":

    parishes = [
        "Andorra la Vella",
        "Canillo",
        "Encamp",
        "Escaldes_Engordany",
        "La Massana",
        "Ordino",
        "Sant julia de Loria",
    ]
    parish = "Andorra la Vella"
    parish_page = "https://en.wikipedia.org/wiki/Andorra_la_Vella"

    gdf_accommodations = gpd.read_file("./data/andorra_accommodations.geojson")
    df_accommodations = gdf_accommodations.drop(columns="geometry")
    gdf_parish_info = gpd.read_file("./data/parish_info.geojson")
    df_parish_info = gdf_parish_info.drop(columns="geometry")

    show_report = False

    accommodation = "total"
    accommodation_type = [
        "total",
        "hotel",
        "apartment",
        "hostel",
    ]

    parishes_dict = {
        "Andorra la Vella": "https://en.wikipedia.org/wiki/Andorra_la_Vella",
        "Canillo": "https://en.wikipedia.org/wiki/Canillo",
        "Encamp": "https://en.wikipedia.org/wiki/Encamp",
        "Escaldes_Engordany": "https://en.wikipedia.org/wiki/Escaldes%E2%80%93Engordany",
        "La Massana": "https://en.wikipedia.org/wiki/La_Massana",
        "Ordino": "https://en.wikipedia.org/wiki/Ordino",
        "Sant julia de Loria": "https://en.wikipedia.org/wiki/Sant_Juli%C3%A0_de_L%C3%B2ria",
    }

    Gui.register_content_provider(JsChartClass, expose_js_chart)
    Gui.register_content_provider(FoliumMap, expose_folium_map)
    Gui.register_content_provider(DeckMap, expose_deck_map)  # Add this for question 3

    gui = Gui(pages=pages)
    gui.run(
        title="Andorra App",
        dark_mode=False,
        favicon="./img/andorra.png",
        use_reloader=True,
    )
