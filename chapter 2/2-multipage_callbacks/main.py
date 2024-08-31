import taipy.gui.builder as tgb
from pages.food_facts import food_fact_page
from pages.unit_converter import converter_page
from pages.welcome import welcome_page
from taipy.gui import Gui, navigate

# Change this to switch menu types:
menu_type_navbar = True


def on_menu(state, var_name, info):
    page = info["args"][0]
    navigate(state, to=page)


with tgb.Page() as root_page:
    tgb.text("# Taipy Food 🍜", mode="md")
    if menu_type_navbar:
        tgb.navbar()
    else:
        tgb.menu(
            label="Navigation_menu",
            lov=[
                ("welcome", "welcome_page"),
                ("unit_converter", "converter_page"),
                ("food_facts", "food_fact_page"),
            ],
            on_action=on_menu,
        )

taipy_food_pages = {
    "/": root_page,
    "welcome": welcome_page,
    "unit_converter": converter_page,
    "food_facts": food_fact_page,
}

taipy_food_gui = Gui(pages=taipy_food_pages)

taipy_food_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Taipy Food 🍜",
    favicon="./images/favicon_burger.png",
    watermark="Taipy food",
    time_zone="UTC",
)
