import taipy.gui.builder as tgb
from algorithms.create_report import create_pdf_report
from taipy.gui import invoke_long_callback, notify


def get_parish(state):
    parishes_dict = {
        "Andorra la Vella": "https://en.wikipedia.org/wiki/Andorra_la_Vella",
        "Canillo": "https://en.wikipedia.org/wiki/Canillo",
        "Encamp": "https://en.wikipedia.org/wiki/Encamp",
        "Escaldes_Engordany": "https://en.wikipedia.org/wiki/Escaldes%E2%80%93Engordany",
        "La Massana": "https://en.wikipedia.org/wiki/La_Massana",
        "Ordino": "https://en.wikipedia.org/wiki/Ordino",
        "Sant julia de Loria": "https://en.wikipedia.org/wiki/Sant_Juli%C3%A0_de_L%C3%B2ria",
    }
    state.parish_page = parishes_dict[state.parish]


def create_report(state):
    invoke_long_callback(
        state, create_pdf_report, [state.df_parish_info], "./pdfs/report.pdf"
    )

    state.show_report = True
    notify(state, "i", "The pdf report is ready!")


with tgb.Page() as parishes_page:
    tgb.text(
        "## Parishes - Accommodation",
        mode="md",
    )

    tgb.button(label="CREATE REPORT!", on_action=create_report)
    with tgb.layout("1 1"):
        tgb.table(data="{df_parish_info}")
        tgb.chart(
            "{df_parish_info}",
            type="bar",
            x="parish",
            y="total",
            title="Total accomodation by Parish",
        )

    tgb.part(page="./pdfs/report.pdf", render="{show_report}", height="500px")

    with tgb.layout("1 1"):
        with tgb.part():
            tgb.selector(
                value="{parish}",
                lov="{parishes}",
                dropdown=True,
                on_change=get_parish,
            )
            tgb.part(page="{parish_page}", height="350px")
        tgb.part(content="{FoliumMap(gdf_accommodations)}", height="350px")
