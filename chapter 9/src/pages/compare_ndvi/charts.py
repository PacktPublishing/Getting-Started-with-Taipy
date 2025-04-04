import pandas as pd
import plotly.express as px
from scipy.signal import savgol_filter


def plot_ndvi_multi_timeseries(df_list, trace_names, title):
    """
    Overlay multiple NDVI time series (different years) on the same x-axis (month-day) to compare trends.

    Args:
        df_list (List[pd.DataFrame]): List of DataFrames (one per year) with NDVI data.
        trace_names (List[str]): Corresponding names for each DataFrame (e.g., years as strings).
        title (str): Plot title.

    Returns:
        plotly.graph_objects.Figure: Overlaid line chart.
    """
    if len(df_list) != len(trace_names):
        raise ValueError("df_list and trace_names must have the same length")

    combined_dfs = []
    for df, name in zip(df_list, trace_names):
        df = df.copy()

        # Convert date column to datetime format
        df["date"] = pd.to_datetime(df["date"])

        # We use 2020 as an arbitrary year for comparison - chart won't show year
        # 2020 is leap year, which could prevent Feb-29 errors
        df["date_std"] = df["date"].apply(lambda x: x.replace(year=2020))

        # Add trace name for identification
        df["trace_name"] = name

        # Append to combined list
        combined_dfs.append(df)

    # Concatenate all the dataframes into one
    combined_df = pd.concat(combined_dfs)

    # Plot using plotly express
    fig = px.line(
        combined_df,
        x="date_std",
        y="ndvi",
        color="trace_name",
        title=f"NDVI Trend Comparison: {title}",
        labels={"ndvi": "NDVI Value", "date_std": "Date (Month-Day)"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    # Update layout to ensure the x-axis is correctly formatted
    fig.update_layout(
        yaxis_title="NDVI Value",
        xaxis_title="Date (Month-Day)",
        yaxis_range=[-1, 1.05],
        hovermode="x unified",
        xaxis_tickformat="%b %d",  # Display only month and day
        xaxis_range=[
            "2020-01-01",
            "2020-12-31",
        ],  # We use arbitrary 2020
    )

    # Add horizontal lines at important NDVI thresholds
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.add_hline(y=0.5, line_dash="dot", line_color="gray")
    fig.add_hline(y=-0.5, line_dash="dot", line_color="gray")

    return fig
