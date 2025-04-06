import taipy.gui.builder as tgb
from pages.general_page.charts import plot_park_with_centroid


def create_park_info_partial(state):
    if state.info_display == "general_info":
        with state as s:
            park_type = state.selected_park_dict.get("type")
            category = state.selected_park_dict.get("category")
            area = state.selected_park_dict.get("area_sqm")
            perimeter = state.selected_park_dict.get("perimeter")
        with tgb.Page() as park_info:
            tgb.text(
                f"""## General Information: {state.selected_park}

- **Park Type:** {park_type}
- **Park Category:** {category}
- **Area:** {area} sqm.
- **Perimeter:** {perimeter} m.
""",
                mode="md",
            )

    elif state.info_display == "map":
        with tgb.Page() as park_info:
            tgb.chart(
                figure=lambda gdf_paris_parks, gdf_paris_parks_centroids, park_id: plot_park_with_centroid(
                    gdf_paris_parks,
                    gdf_paris_parks_centroids,
                    park_id,
                )
            )
    else:
        print("wrong partial selection")
        with tgb.Page() as park_info:
            tgb.text(
                "There was a problem generating partial. Contact support.", mode="md"
            )

    state.park_partial.update_content(state, park_info)
