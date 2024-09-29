import taipy as tp
import taipy.gui.builder as tgb
from orchestration import biggest_cities, world_countries_area, world_countries_pop

selected_data_node = world_countries_area

df_countries = selected_data_node.read()


def change_data_node(state, var_name, value):
    print(value)
    state.df_countries = state.selected_data_node.read()


# state.selected_data = value.read()


#############################
##           Page          ##
#############################

with tgb.Page() as data_node_selector:
    tgb.text("## Discovering Node selectors", mode="md")

    tgb.data_node_selector(value="{selected_data_node}", on_change=change_data_node)

    tgb.table(data="{df_countries}", rebuild=True)
