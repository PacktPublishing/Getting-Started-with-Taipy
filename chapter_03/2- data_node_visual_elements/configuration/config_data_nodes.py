import io

import pandas as pd
import requests
from bs4 import BeautifulSoup
from taipy import Config, Orchestrator, Scope


def get_wiki_table(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})

    df_cities = pd.read_html(io.StringIO(str(table)))[0]

    return df_cities


world_countries_area_config = Config.configure_generic_data_node(
    id="area_per_country",
    read_fct=get_wiki_table,
    read_fct_args=[
        "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
    ],
    scope=Scope.GLOBAL,
)

world_countries_pop_config = Config.configure_generic_data_node(
    id="population_per_country",
    read_fct=get_wiki_table,
    read_fct_args=[
        "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
    ],
    scope=Scope.GLOBAL,
)

cities_csv_node_config = Config.configure_csv_data_node(
    id="most_populated_cities_csv",
    default_path="../data/cities.csv",
    has_header=True,
    exposed_type="pandas",
    scope=Scope.GLOBAL,
)
