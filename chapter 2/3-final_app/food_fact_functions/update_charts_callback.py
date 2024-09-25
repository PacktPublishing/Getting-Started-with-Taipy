from food_fact_functions.charts import create_fig_states


def update_charts(state, var_name):
    # force reload of charts:
    state.df_sales = state.df_sales

    state.fig_states = create_fig_states(state.df_sales, state.metric)
