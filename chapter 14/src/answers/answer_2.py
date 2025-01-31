import tempfile

import folium
from folium.plugins import Fullscreen, Geocoder


class FoliumMap:
    def __init__(self, gdf, parish):
        self.gdf = gdf
        self.parish = parish
        self.map = self.create_accommodations_map()

    def create_accommodations_map(self):
        """
        Creates a Folium map with markers for accommodations, differentiated by type.
        """
        gdf = self.gdf
        gdf = gdf[gdf.parish == self.parish]
        # Central point for the map using average of x and y
        if gdf.empty:
            raise ValueError("GeoDataFrame is empty. Cannot create a map.")

        center_lat = gdf["latitude"].mean()
        center_lon = gdf["longitude"].mean()

        folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)

        Geocoder().add_to(folium_map)
        Fullscreen().add_to(folium_map)

        # Add markers to the map - define function to use apply()
        def add_marker(row):
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
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<b>{row['name']}</b><br>Type: {row['type']}<br>Street: {row['street']}<br>Website: {row['website']}",
                icon=folium.Icon(color=marker_colors.get(row["parish"], "gray")),
            ).add_to(folium_map)

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
