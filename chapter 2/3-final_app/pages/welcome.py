import pandas as pd
import taipy.gui.builder as tgb

url_image = "https://images.unsplash.com/photo-1485962398705-ef6a13c41e8f?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
with open("description.md", "r") as description:
    description_text = description.read()

# Open Pane
open_pane = False  # set to True to see display


def open_pane_callback(state):
    state.open_pane = True


## Upload file with restarants
favorite_restaurants_url = None
favorite_restaurants = pd.DataFrame()


def upload_restaurants(state):
    state.favorite_restaurants = pd.read_csv(state.favorite_restaurants_url)


with tgb.Page() as welcome_page:
    with tgb.pane(open="{open_pane}"):
        tgb.text("## Contact information", mode="md", class_name="color-secondary")
        tgb.text("taipy_food@taipy_food.com")

    with tgb.layout("1 3"):
        with tgb.part(class_name="sidebar"):
            tgb.text(
                "## Why Choose Taipy Food?",
                mode="md",
                class_name="color-secondary header",
            )
            tgb.text(
                "It’s the ultimate tool for making cooking easier and more fun! ",
                mode="md",
                class_name="container",
            )
            tgb.image(
                url_image,
                width="200px",
            )
            tgb.button(
                label="Show Contacts",
                on_action=open_pane_callback,
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
            with tgb.expandable("Favorite Restaurants", expanded=False):
                tgb.file_selector(
                    content="{favorite_restaurants_url}",
                    label="Upload restaurants",
                    on_action=upload_restaurants,
                    extensions=".csv",
                    drop_message="Yum Yum!",
                )
                tgb.table("{favorite_restaurants}", height="60vh", rebuild=True)
