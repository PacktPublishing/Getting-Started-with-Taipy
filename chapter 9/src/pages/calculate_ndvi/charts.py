import pandas as pd
import plotly.express as px


def plot_box(ndvi_array, id_name):
    """
    Creates violin plot of the NDVI median yearly array.

    Args:
    ndvi_array : numpy.ndarray
        Array wuth NDVI values
    id_name : str
        Name and id of the park

    Returns:
    violin plot plotly figure
    """
    flattened_data = ndvi_array.flatten()

    fig = px.violin(
        y=flattened_data,
        title=f"NDVI distribution for {id_name}",
        labels={"y": "NDVI"},
        color_discrete_sequence=["#12b049"],
    )

    fig.update_layout(
        showlegend=False,
        yaxis_title="NDVI Value",
        xaxis_title="",
        plot_bgcolor="rgba(240,240,240,0.8)",
        paper_bgcolor="rgba(240,240,240,0.5)",
        font=dict(family="Arial", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # NDVI range for scale: (-1 to 1)
    fig.update_yaxes(range=[-1, 1])

    # Add horizontal lines at important NDVI thresholds
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.add_hline(y=0.5, line_dash="dot", line_color="gray")
    fig.add_hline(y=-0.5, line_dash="dot", line_color="gray")

    return fig


def plot_ndvi(np_image, title):
    """
    Create an NDVI image from a NumPy Array.
    Args:
        np_image: np.ndarray: A NumPy array with median season values
            for each pixel.
    Returns:
        Plotly imshow figure
    """
    fig = px.imshow(
        np_image,
        color_continuous_scale="RdYlGn",
        range_color=(-1, 1),
        labels={"color": "NDVI"},
    )
    fig.update_traces(
        hovertemplate="NDVI: %{z}<extra></extra>",  # `%{z}` is the value, `<extra></extra>` removes secondary hover info
    )
    fig.update_layout(
        title=f"NDVI Map - {title}", coloraxis_colorbar=dict(title="NDVI")
    )
    return fig


def plot_ndvi_timeseries(df, title):
    """
    Line plot for time series DataFrame. The plot has indicator lines
    for healthy vegetation and for non-vegetation index rates.

    Args:
        df : DataFrame
            NDVI time series with a 'date' column.
        title : str
            Title for the plot.

    Returns:
        plotly.graph_objects.Figure
            Line chart for the time series.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(
        df["date"]
    ).dt.date  # Convert to date format (remove time)

    title = f"NDVI Trend: {title}"

    fig = px.line(
        df,
        x="date",
        y="ndvi",
        title=title,
        labels={"ndvi": "NDVI Value", "date": "Date"},
        color_discrete_sequence=["#12b049"],
        template="plotly_white",
    )

    fig.update_traces(
        line_width=2.5,
        hovertemplate="<b>Date</b>: %{x|%b %d}<br><b>NDVI</b>: %{y:.2f}",
        mode="lines",
    )

    fig.update_layout(
        yaxis_title="NDVI Value",
        xaxis_title="",
        yaxis_range=[-1, 1.05],
        hovermode="x unified",
        plot_bgcolor="white",
        font=dict(family="Arial"),
        margin=dict(l=50, r=50, t=60, b=30),
    )

    # NDVI reference lines
    for y, color, name in [
        (0.5, "#8BC34A", "Healthy"),
        (0, "#FFC107", "Neutral"),
        (-0.2, "#F44336", "Barren"),
    ]:
        fig.add_hline(
            y=y,
            line_dash="dot",
            line_color=color,
            opacity=0.5,
            annotation_text=name,
            annotation_position="right",
            annotation_font_size=10,
        )

    return fig
