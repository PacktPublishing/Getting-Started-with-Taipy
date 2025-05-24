import tempfile

import pydeck as pdk


def _calculate_centroids(gdf):
    """Polygon centroids need a projected CRS"""
    gdf_projected = gdf.to_crs(epsg=25831)
    gdf_projected["centroid"] = gdf_projected.geometry.centroid
    gdf_projected = gdf_projected.set_geometry("centroid").to_crs(epsg=4326)
    gdf["latitude"] = gdf_projected.geometry.y
    gdf["longitude"] = gdf_projected.geometry.x
    return gdf


class DeckMap:
    def __init__(self, gdf):
        self.gdf = gdf
        self.map = self.create_3d_column_map()

    def create_3d_column_map(self):
        gdf = self.gdf
        gdf = _calculate_centroids(gdf)

        column_layer = pdk.Layer(
            "ColumnLayer",
            gdf,
            get_position=["longitude", "latitude"],
            get_elevation="total * 500",
            get_fill_color="[200, total * 10, 150, 200]",
            radius=500,
            elevation_scale=1,
            extruded=True,
            pickable=True,
        )

        view_state = pdk.ViewState(latitude=42.5, longitude=1.5, zoom=10, pitch=45)

        deck = pdk.Deck(
            layers=[column_layer],
            initial_view_state=view_state,
            tooltip={"text": "{parish}\nTotal Accomodations: {total}"},
        )

        return deck


def expose_deck_map(deck_map: DeckMap) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        deck_map.map.to_html(temp_file.name)
        with open(temp_file.name, "rb") as f:
            return f.read()
