import pandas as pd
import requests
import taipy as tp
from bs4 import BeautifulSoup
from taipy import Config, Core, Scope


def get_wiki_table(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})

    df_cities = pd.read_html(io.StringIO(str(table)))[0]

    return df_cities


cities_url_node_config = Config.configure_generic_data_node(
    id="cities_from_wikipedia",
    read_fct=get_wiki_table,
    read_fct_args=["https://en.wikipedia.org/wiki/List_of_largest_cities"],
    write_fct_args=None,
    scope=Scope.GLOBAL,
)

core = Core()
core.run()
cities_url_data_node = tp.create_global_data_node(cities_url_node_config)

df_cities = cities_url_data_node.read()

print(df_cities.head())
