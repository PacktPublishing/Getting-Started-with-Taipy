import tempfile

import folium
from folium.plugins import MarkerCluster


class FoliumMap:
    def __init__(self, gdf):
        self.gdf = gdf
        self.map = self.create_accommodations_map()

    def create_accommodations_map(self):
        """
        Creates a Folium map with markers for accommodations, differentiated by type.
        """
        gdf = self.gdf
        # Central point for the map using average of x and y
        if gdf.empty:
            raise ValueError("GeoDataFrame is empty. Cannot create a map.")

        center_lat = gdf["latitude"].mean()
        center_lon = gdf["longitude"].mean()

        folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)

        # Group Markers in cluster when the zoom is out
        marker_cluster = MarkerCluster().add_to(folium_map)

        # Define marker colors based on accommodation type
        marker_colors = {
            "Andorra la Vella": "blue",
            "Canillo": "green",
            "Encamp": "red",
            "Escaldes-Engordany": "black",
            "La Massana": "purple",
            "Ordino": "pink",
            "Sant Julia de Loria": "orange",
        }

        # Add markers to the map - define function to use apply()
        def add_marker(row):
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<b>{row['name']}</b><br>Type: {row['type']}<br>Street: {row['street']}<br>Website: {row['website']}",
                icon=folium.Icon(color=marker_colors.get(row["type"], "gray")),
            ).add_to(marker_cluster)

        gdf.apply(add_marker, axis=1)

        return folium_map


def expose_folium_map(folium_map: FoliumMap) -> str:
    """
    Exposes the generated chart page to Taipy as HTML content.

    Args:
        folium_map (JsChartClass): The chart object containing the HTML content.

    Returns:
        Folium Map.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        folium_map.map.save(temp_file.name)
        with open(temp_file.name, "rb") as f:
            return f.read()
