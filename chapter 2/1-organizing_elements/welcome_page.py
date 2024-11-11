import taipy.gui.builder as tgb

# original image from:
# url_image = "https://images.unsplash.com/photo-1485962398705-ef6a13c41e8f?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

url_image = "./images/food.avif"

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
