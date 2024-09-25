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
## Main Callback         ##
###########################


def update_sales(state, var_name, payload):
    df_sales_copy = update_df_sales(state.df_sales_original, state.adjust_inflation)

    filter_condition = pd.Series([True] * len(df_sales_copy))
    if state.selected_year != "All":
        filter_condition &= df_sales_copy["Year"] == state.selected_year

    # We add the "empty" states too, to see the added rows, that don't have any state
    filter_condition &= df_sales_copy["State"].isin(state.selected_states) | (
        df_sales_copy["State"].isnull()
    )

    df_sales_copy = df_sales_copy.loc[filter_condition]

    state.df_sales = df_sales_copy

    state.fig_states = create_fig_states(state.df_sales, state.metric)


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
            # mode="checkbox",
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

        tgb.toggle(value="{metric}", lov=lov_metrics, on_change=update_sales)

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
            class_name="p0 m0",
            rebuild=True,
        )
        tgb.chart(
            data="{df_sales}",
            type="heatmap",
            x="State",
            y="Year",
            z="{metric}",
            title="Value per year and State",
            class_name="p0 m0",
            rebuild=True,
        )

        tgb.chart(
            figure="{fig_states}",
            class_name="p0 m0",
        )

    tgb.table(
        data="{df_sales}",
        height="60vh",
        filter=True,
        hover_text="USDA Data ",
        on_edit=edit_note,
        on_add=add_row,
        on_delete=delete_row,
        class_name="p0 m0",
        nan_value=0,
    )
