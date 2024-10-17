import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb


def edit_row(state, var_name, payload):
    df_cities_cp = state.df_cities
    df_cities_cp.loc[payload["index"], payload["col"]] = payload["value"]
    state.df_cities = df_cities_cp

    biggest_cities.write(state.df_cities)


with tgb.Page() as simple_data_node:
    tgb.text("## Interacting with a Data Node from the GUI", mode="md")

    tgb.table(
        data="{df_cities}", filter=True, editable=True, on_edit=edit_row, rebuild=True
    )
