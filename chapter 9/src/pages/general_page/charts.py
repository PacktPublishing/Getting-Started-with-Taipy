import plotly.express as px


def plot_park_with_centroid(
    gdf_parks, gdf_park_centroid, park_id, map_style="open-street-map"
):
    """
    Plots a specific park with its centroid on a Plotly map.

    Args:
        gdf_parks (geopandas.GeoDataFrame): GeoDataFrame containing park polygons.
        gdf_park_centroid (geopandas.GeoDataFrame): GeoDataFrame containing park centroids.
        park_id (str or int): The ID of the park to plot.
        map_style (str, optional): Map style. Defaults to "open-street-map".

    Returns:
        plotly.graph_objects.Figure: A Plotly map figure, or None if the park is not found.
    """

    park_polygon = gdf_parks[gdf_parks["id"] == park_id].copy()
    park_centroid = gdf_park_centroid[gdf_park_centroid["id"] == park_id].copy()

    if park_polygon.empty or park_centroid.empty:
        return None

    # Get centroid coordinates
    centroid_point = park_centroid["geometry"].iloc[0]
    center = {"lat": centroid_point.y, "lon": centroid_point.x}

    fig = px.choropleth_map(
        park_polygon,
        geojson=park_polygon.geometry.__geo_interface__,
        locations=park_polygon.index,
        center=center,
        map_style=map_style,
        zoom=15,
        opacity=0.5,
        hover_name="name",
        hover_data={
            "name": True,
            "type": True,
            "category": True,
            "area_sqm": True,
        },
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
