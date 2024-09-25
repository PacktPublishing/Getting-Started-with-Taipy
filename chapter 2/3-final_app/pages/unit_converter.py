import taipy.gui.builder as tgb
from food_converter_functions.change_volume_callback import change_volume
from food_converter_functions.change_weight_callback import change_weight
from food_converter_functions.reset_callback import reset

###########################
## Initial values        ##
###########################
grams = cups = ounces = tablespoons = teaspoons = milliliters = 0


###########################
## Page                  ##
###########################

with tgb.Page() as converter_page:  # food_fact_page for food_facts.py
    tgb.text("# Unit converter 🧮", mode="md")

    tgb.text("## Volume units", mode="md", class_name="color-secondary header")
    with tgb.layout("1 1 1 1"):
        tgb.number(value="{cups}", label="Cups", on_change=change_volume)
        tgb.number(value="{tablespoons}", label="Tablespoons", on_change=change_volume)
        tgb.number(value="{teaspoons}", label="Teaspoons", on_change=change_volume)
        tgb.number(value="{milliliters}", label="Millilliters", on_change=change_volume)

    tgb.text("## Weight units", mode="md", class_name="color-secondary header")
    with tgb.layout("1 1 1 1"):
        tgb.number(value="{grams}", label="Grams", on_change=change_weight)
        tgb.number(value="{ounces}", label="Ounces", on_change=change_weight)

        with tgb.layout("1 1"):
            tgb.button(
                label="Reset weight values",
                on_action=reset,
                id="reset_weight",
            )
            tgb.button(label="Reset volume values", on_action=reset, id="reset_volume")

        tgb.button(
            label="Reset all values",
            on_action=reset,
            id="reset_all",
        )

        tgb.text("{grams} grams is {grams/1000} kilograms", mode="md")
