import plotly.express as px


def create_weekday_chart(df_time, y_axis, break_by="All"):
    """
    Creates a bar chart for sales by weekday, optionally broken down by a specific column.

    Args:
        df_time (pandas.DataFrame): The input DataFrame.
        y_axis (str): The column name for the y-axis.
        break_by (str): The column to group by. Defaults to "All".

    Returns:
        plotly.graph_objects.Figure: The resulting bar chart.
    """
    color = break_by if break_by != "All" else None
    barmode = "stack" if break_by != "All" else None
    title = f"Sales by Weekday{' by ' + break_by if break_by != None else ''}"

    fig = px.bar(
        df_time,
        x="day",
        y=y_axis,
        color=color,
        barmode=barmode,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def create_time_scatter(df_time, y_axis, break_by="All"):
    """
    Creates a scatter chart showing sales over time.

    Args:
        df_time (pandas.DataFrame): The input DataFrame containing 'date' and the target column.
        y_axis (str): The column name for the y-axis.
        break_by (str): The column to break lines by. Defaults to "All".

    Returns:
        plotly.graph_objects.Figure: The resulting scatter chart.
    """
    color = break_by if break_by != "All" else None
    title = f"Sales Over Time{' by ' + break_by if break_by != None else ''}"

    fig = px.line(
        df_time,
        x="date",
        y=y_axis,
        color=color,
        title=title,
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def create_customer_heatmap(df_customer, z_axis):
    """
    Creates a density heatmap showing sales by customer type.

    Args:
        df_customer (pandas.DataFrame): The input DataFrame containing customer data.
        z_axis (str): The column name for the z-axis, representing the value to aggregate.

    Returns:
        plotly.graph_objects.Figure: The resulting heatmap.

    This function generates a heatmap where:
        - The x-axis represents customer generations.
        - The y-axis represents customer genders.
        - The z-axis aggregates the specified column values.
    """
    if df_customer.empty or z_axis not in df_customer.columns:
        # Handle exceptions. Here: empty DataFrame or missing z-axis column
        return None
    fig = px.density_heatmap(
        df_customer,
        x="generation",
        y="gender",
        z=z_axis,
        title="Sales by customer type",
        color_continuous_scale="algae",
    )
    return fig


def create_product_chart(df_product, y_axis):

    fig = px.bar(
        df_product,
        x="type",
        y=y_axis,
        color="color",
        barmode="stack",
        title="Sales by byke type and color",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def plot_forecast(df_agg, target, forecast_df):
    """
    Plots the actual and forecasted values with confidence intervals.

    Parameters:
        df_agg (pd.DataFrame): Historical data with actual values.
        target (str): Name of the target column.
        forecast_df (pd.DataFrame): Dataframe with forecasted values and confidence intervals.

    Returns:
        plotly.express fig.
    """
    df_agg_reset = df_agg.reset_index().rename(columns={"index": "date"})
    fig = px.line(
        df_agg_reset, x="date", y=target, title=f"{target.capitalize()} Forecast"
    )
    fig.add_scatter(
        x=forecast_df["date"], y=forecast_df["forecast"], mode="lines", name="Forecast"
    )
    fig.add_scatter(
        x=forecast_df["date"],
        y=forecast_df["conf_min"],
        mode="lines",
        name="Lower Bound",
        line=dict(dash="dash"),
    )
    fig.add_scatter(
        x=forecast_df["date"],
        y=forecast_df["conf_max"],
        mode="lines",
        name="Upper Bound",
        line=dict(dash="dash"),
    )
    return fig
