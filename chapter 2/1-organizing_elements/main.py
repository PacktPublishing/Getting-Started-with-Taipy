from datetime import datetime

import taipy.gui.builder as tgb
from taipy.gui import Gui

url_image = "https://images.unsplash.com/photo-1485962398705-ef6a13c41e8f?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
with open("description.md", "r") as description:
    description_text = description.read()

open_pane = True  # set to True to see display

with tgb.Page() as welcome_page:
    with tgb.pane(open=open_pane):
        tgb.text("## Contact information", mode="md")
        tgb.text("taipy_food@taipy_food.com")

    tgb.text("# Taipy Food 🍜", mode="md")
    with tgb.layout("1 3"):
        with tgb.part():
            tgb.text("## Why Choose Taipy Food?", mode="md")
            tgb.text(
                "It’s the ultimate tool for making cooking easier and more fun!",
                mode="md",
            )
            tgb.image(
                url_image,
                width="200px",
            )
        with tgb.part():
            tgb.text(description_text, mode="md")
            with tgb.expandable("External Resources", expanded=False):
                tgb.text(
                    "* [Food and Agriculture organization (FAO)](https://www.fao.org/)",
                    mode="md",
                )
                tgb.text(
                    "* [United States Department of Agriculture (USDA)](https://www.usda.gov/)",
                    mode="md",
                )
taipy_food_gui = Gui(page=welcome_page)

taipy_food_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Taipy Food 🍜",
    favicon="./images/favicon_burger.png",
    watermark="Taipy food",
)
