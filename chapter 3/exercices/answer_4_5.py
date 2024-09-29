import taipy as tp
import taipy.gui.builder as tgb
from food_fact_functions.initiate_sales import clean_sales_data, update_df_sales
from taipy import Config, Orchestrator, Scope
from taipy.gui import Gui

#######################################
### ANSWER 4 STARTS HERE             ##
#######################################
sales_csv_file = "./data/state_sales.csv"

sales_configuration_file = Config.configure_generic_data_node(
    id="cities_from_wikipedia",
    read_fct=clean_sales_data,
    read_fct_args=[sales_csv_file],
    write_fct_args=None,
    scope=Scope.GLOBAL,
)


orchestrator = Orchestrator()
orchestrator.run()
sales_data_node = tp.create_global_data_node(sales_configuration_file)

df_sales_original = sales_data_node.read()

#######################################
### ANSWER 4 ENDS HERE               ##
#######################################

## First: pre-process the data fro the DataFrame

df_sales_original = clean_sales_data(sales_csv_file)
df_sales = update_df_sales(df_sales_original)


###########################
## Page                 ##
###########################


with tgb.Page() as food_fact_page:
    tgb.text("# Food facts 📊", mode="md", class_name="color-secondary header")

    #######################################
    ### ANSWER 5 STARTS HERE             ##
    #######################################
    ## Old table, for reference:
    """
    tgb.table(
        data="{df_sales}",
        height="60vh",
        filter=True,
        hover_text="USDA Data ",
        # on_edit=edit_note,
        # on_add=add_row,
        # on_delete=delete_row,
        class_name="p0 m0",
        nan_value=0,
    )
    """
    tgb.data_node(
        "{sales_data_node}",
        show_properties=False,
        show_history=False,
        show_owner=False,
        show_config=False,
    )

#######################################
### ANSWER 5 Ends HERE               ##
#######################################

gui_page = Gui(page=food_fact_page)

gui_page.run(use_reloader=True)
