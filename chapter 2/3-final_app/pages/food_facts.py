import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import us
from food_fact_functions.add_row_callback import add_row
from food_fact_functions.charts import create_fig_states
from food_fact_functions.delete_row_callback import delete_row
from food_fact_functions.edit_note_callback import edit_note
from food_fact_functions.initiate_sales import clean_sales_data, update_df_sales
from food_fact_functions.open_state_selector_callback import open_state_selector
from food_fact_functions.update_charts_callback import update_charts
from food_fact_functions.update_sales_callback import update_sales

###########################
## Initial values        ##
###########################

## First: pre-process the data fro the DataFrame
sales_csv_file = "./data/state_sales.csv"

df_sales_original = clean_sales_data(sales_csv_file)
df_sales = update_df_sales(df_sales_original)


adjust_inflation = False

lov_year = list(df_sales["Year"].astype(str).unique())
lov_year.append("All")
selected_year = "All"


# To open the pane for states:
open_states = False
lov_states = list(df_sales["State"].unique())
selected_states = lov_states

lov_metrics = ["FAH", "FAFH", "Total"]
metric = "Total"


fig_states = create_fig_states(df_sales, "Total")

###########################
## Page                 ##
###########################


with tgb.Page() as food_fact_page:
    tgb.text("# Food facts 📊", mode="md", class_name="color-secondary header")

    with tgb.pane(open="{open_states}"):
        tgb.text("## Select states", mode="md", class_name="color-secondary")
        tgb.selector(
            value="{selected_states}",
            lov="{lov_states}",
            on_change=update_sales,
            label="select states",
            multiple=True,
            mode="checkbox",
        )

    with tgb.layout("1 1 1 1"):

        tgb.button(label="select states", on_action=open_state_selector)

        tgb.selector(
            value="{selected_year}",
            lov="{lov_year}",
            on_change=update_sales,
            label="select year",
            dropdown=True,
        )

        tgb.toggle(value="{metric}", lov=lov_metrics, on_change=update_charts)

        tgb.toggle(
            value="{adjust_inflation}",
            label="Adjust for inflation",
            on_change=update_sales,
        )

    with tgb.layout("1 1 1"):
        tgb.chart(
            data="{df_sales}",
            type="bar",
            x="State",
            y="{metric}",
            title=f"Value per State",
            rebuild=True,
        )
        tgb.chart(
            data="{df_sales}",
            type="heatmap",
            x="State",
            y="Year",
            z="{metric}",
            title="Value per year and State",
            rebuild=True,
        )

        tgb.chart(
            figure="{fig_states}",
        )

    tgb.table(
        data="{df_sales}",
        height="60vh",
        filter=True,
        editable=True,
        hover_text="USDA Data ",
        on_edit=edit_note,
        on_add=add_row,
        on_delete=delete_row,
        nan_value=0,
    )
