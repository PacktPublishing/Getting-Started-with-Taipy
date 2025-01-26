import taipy.gui.builder as tgb

with tgb.Page() as general_info:
    tgb.text(
        "## General Information",
        mode="md",
    )

    with tgb.layout("1 1"):
        tgb.part(page="./iframes/andorra_presentation.html", height="500px")
        tgb.part(page="./pdfs/constitucio_en.pdf", height="500px")
