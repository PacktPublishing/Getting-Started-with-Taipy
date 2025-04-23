from food_fact_functions.charts import create_fig_states
from taipy.gui import notify


def update_charts(state, var_name, payload):
    # force reload of charts:
    state.df_sales = state.df_sales

    state.fig_states = create_fig_states(state.df_sales, state.metric)
    notify(state, notification_type="success", message=f"Selected metric: {payload}")
