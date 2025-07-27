from algorithms.create_report import create_pdf_report

import taipy.gui.builder as tgb
from taipy.gui import invoke_long_callback, notify


def update_pdf_part(state, is_finished):
    if is_finished:
        state.show_report = True
        notify(state, "i", "The pdf report is ready!")


def create_report(state):
    invoke_long_callback(
        state, create_pdf_report, [state.df_parish_info], update_pdf_part
    )


with tgb.Page() as parishes_page:
    tgb.text(
        "## Parishes - Accommodation",
        mode="md",
    )

    tgb.button(
        label="CREATE REPORT!",
        on_action=create_report,
        class_name="fullwidth plain",
    )
    with tgb.layout("1 1"):
        tgb.table(data="{df_parish_info}")
        tgb.chart(
            "{df_parish_info}",
            type="bar",
            x="parish",
            y="total",
            title="Total accomodation by Parish",
        )

    tgb.part(page="./iframes/report.pdf", render="{show_report}", height="500px")

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.selector(
                value="{parish}",
                lov="{parishes}",
                dropdown=True,
                class_name="fullwidth",
            )
            tgb.part(page="{parishes_dict.get(parish)}", height="340px")
        tgb.part(content="{FoliumMap(gdf_accommodations)}", height="350px")
