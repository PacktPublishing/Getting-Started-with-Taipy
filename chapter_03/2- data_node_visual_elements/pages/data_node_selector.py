import taipy as tp
import taipy.gui.builder as tgb

#############################
##           Page          ##
#############################

with tgb.Page() as data_node_selector:
    tgb.text("## Discovering Node selectors", mode="md")

    tgb.data_node_selector(
        value="{selected_data_node}",
        on_change=lambda state: state.selected_data_node.read(),
    )

    tgb.table(data="{selected_data_node.read()}", rebuild=True)
