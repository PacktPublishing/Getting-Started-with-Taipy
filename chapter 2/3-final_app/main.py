import taipy.gui.builder as tgb
from pages.food_facts import food_fact_page
from pages.unit_converter import converter_page
from pages.welcome import welcome_page
from taipy.gui import Gui, navigate
from taipy.gui.icon import Icon

# Change this to switch menu types:
menu_type_navbar = False


def on_menu(state, var_name, info):
    page = info["args"][0]
    navigate(state, to=page)


with tgb.Page() as root_page:
    tgb.toggle(theme=True)
    tgb.text("# Taipy Food 🍜", mode="md", class_name="color-primary")

    with tgb.layout("1 1"):
        if menu_type_navbar:
            tgb.navbar()
        else:
            tgb.menu(
                label="Navigation_menu",
                lov=[
                    (
                        "welcome",
                        Icon(
                            path="./images/utensils_dark.png",
                            text="Welcome!",
                        ),
                    ),
                    (
                        "unit_converter",
                        Icon(
                            path="./images/scale_dark.png",
                            text="Conerverter Page!",
                        ),
                    ),
                    (
                        "food_facts",
                        Icon(
                            path="./images/chart_dark.png",
                            text="Food Price Facts",
                        ),
                    ),
                ],
                on_action=on_menu,
            )


taipy_food_pages = {
    "/": root_page,
    "welcome": welcome_page,
    "unit_converter": converter_page,
    "food_facts": food_fact_page,
}

stylekit = {
    "color_primary": "#E91E63",  # hot pink
    "color_secondary": "#00BCD4",  # aqua blue
}

taipy_food_gui = Gui(pages=taipy_food_pages, css_file="./css/main.css")

if __name__ == "__main__":
    taipy_food_gui.run(
        use_reloader=True,
        dark_mode=False,
        title="Taipy Food 🍜",
        favicon="./images/favicon_burger.png",
        watermark="Taipy food",
        stylekit=stylekit,
    )
