import taipy.gui.builder as tgb
from pages.general_page.park_partial import create_park_info_partial


def change_selection(state):
    with state as s:
        if s.selected_park:  # Avoid doing anything if empty string
            park = s.selected_park
            s.park_id = int(park.split("-")[0])

            df_parks_cp = s.df_paris_parks.copy()
            s.selected_park_row = df_parks_cp[df_parks_cp["id"] == s.park_id]
            s.selected_park_dict = s.selected_park_row.to_dict(orient="records")[0]
            create_park_info_partial(s)


with tgb.Page() as general_page:
    tgb.text("## **General** information", mode="md")
    tgb.html("hr")

    with tgb.expandable("Parks Summary"):
        with tgb.layout("1 1 1"):
            tgb.metric("{number_parks}", title="Total Number of Parks", type=None)
            tgb.metric(
                "{number_parks_over_100}",
                title="Number of Parks over 100m2",
                type=None,
            )
            tgb.metric(
                "{number_parks_over_1_000}",
                title="Number of Parks over 1,000 m2",
                type=None,
            )
            tgb.chart(
                "{df_types}",
                type="bar",
                x="type",
                y="count",
                title="Number of garden by type",
                color="#12b049",
            )
            tgb.chart(
                "{df_categories}", type="bar", x="category", y="count", color="#12b049"
            )
            tgb.part(page="./widgets/paris_parks_widget.html", height="420px")

        tgb.table("{df_paris_parks}", page_size=25, filter=True)

    with tgb.expandable("Park Info"):

        with tgb.layout("1 1"):
            tgb.selector(
                "{selected_park}",
                lov="{id_name_list}",
                label="Select park",
                dropdown=True,
                filter=True,
                on_change=change_selection,
            )
            tgb.toggle(
                "{info_display}",
                lov=["general_info", "map"],
                on_change=change_selection,
            )

        tgb.part(partial="{park_partial}")
