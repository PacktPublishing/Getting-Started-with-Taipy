import plotly.express as px


def create_earthquake_map(df):
    """
    Create a Plotly map figure for earthquake data.

    Parameters:
        df (pd.DataFrame): DataFrame containing earthquake data with columns:
            - latitude: Latitude of the earthquake.
            - longitude: Longitude of the earthquake.
            - mag: Magnitude of the earthquake.
            - place: Location description of the earthquake.
            - time: Timestamp of the earthquake.

    Returns:
        fig (plotly.graph_objects.Figure): A Plotly map figure.
    """
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="mag",
        size="mag",
        hover_name="place",
        hover_data={"time": True, "mag": True, "latitude": True, "longitude": True},
        color_continuous_scale=px.colors.sequential.Jet,
        range_color=[0, 10],  # Force consistent scale
        zoom=1,
        height=600,
        title="Earthquake Map",
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )

    return fig
