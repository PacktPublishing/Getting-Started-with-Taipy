import plotly.express as px


def create_fig_states(df_sales, metric):
    fig_states = px.choropleth(
        df_sales,
        locations="State_Code",
        locationmode="USA-states",
        color=metric,
        title=f"Values per state for {metric} sales",
        scope="usa",
        color_continuous_scale=px.colors.sequential.ice_r,
    )
    return fig_states
