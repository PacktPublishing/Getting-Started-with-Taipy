import pandas as pd
from food_fact_functions.charts import create_fig_states
from food_fact_functions.initiate_sales import update_df_sales


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
