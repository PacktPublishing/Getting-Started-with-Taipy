from sre_parse import State

import taipy.gui.builder as tgb

###########################
## Initial values        ##
###########################
grams = cups = ounces = tablespoons = teaspoons = milliliters = 0


###########################
## Callbacks             ##
###########################
def change_weight(state, var_name, value):
    if var_name == "grams":  # Grams to Ounces
        state.ounces = round(value / 28.35, 2)
    else:  # Ounces to Grams
        state.grams = round(value * 28.35, 2)


def change_volume(state, var_name, value):
    if var_name == "cups":
        state.tablespoons = round(value * 16, 2)
        state.milliliters = round(value * 236.6, 2)
        state.teaspoons = round(value * 48, 2)
    elif var_name == "tablespoons":
        state.cups = round(value / 16, 2)
        state.milliliters = round(value * 14.787, 2)
        state.teaspoons = round(value * 3, 2)
    elif var_name == "milliliters":
        state.tablespoons = round(value / 14.787, 2)
        state.cups = round(value / 236.6, 2)
        state.teaspoons = round(value / 4.929, 2)
    elif var_name == "teaspoons":
        state.milliliters = round(value * 4.929, 2)
        state.cups = round(value / 48, 2)
        state.tablespoons = round(value / 3, 2)


def reset(state, id, payload):

    state.grams = 0
    state.cups = 0
    state.ounces = 0
    state.tablespoons = 0
    state.teaspoons = 0
    state.milliliters = 0


with tgb.Page() as converter_page:  # food_fact_page for food_facts.py
    tgb.text("# Unit converter 🧮", mode="md")

    # tgb.text("# Food facts 📊", mode="md") #For food_facts.py

    tgb.text("## Volume units", mode="md")
    with tgb.layout("1 1 1 1"):
        tgb.number(value="{cups}", label="Cups", on_change=change_volume, min=0)
        tgb.number(
            value="{tablespoons}", label="Tablespoons", on_change=change_volume, min=0
        )
        tgb.number(
            value="{teaspoons}", label="Teaspoons", on_change=change_volume, min=0
        )
        tgb.number(
            value="{milliliters}", label="Millilliters", on_change=change_volume, min=0
        )

    tgb.text("## Weight units", mode="md")
    with tgb.layout("1 1 1 1"):
        tgb.number(value="{grams}", label="Grams", on_change=change_weight, min=0)
        tgb.number(value="{ounces}", label="Ounces", on_change=change_weight, min=0)

        with tgb.layout("1 1"):
            tgb.button(
                label="Reset weight values",
                on_action=reset,
                id="reset_weight",
            )
            tgb.button(label="Reset volume values", on_action=reset, id="reset_volume")

        tgb.button(label="Reset all values", on_action=reset, id="reset_all")

        tgb.text("{grams} grams is {grams/1000} kilograms", mode="md")
