from taipy import Gui
from taipy.designer import Page


def convert_currency(currency, rate):
    """Converts Euros to US Dollars."""
    return currency * rate


## Callback ##
def on_change(state, var, val):
    if var == "usd_to_eur_rate":
        state.eur_to_usd_rate = 1 / state.usd_to_eur_rate

    # Regarless of callback origin, update:
    if state.unit == "usd":
        state.converted_value = state.value_to_convert * state.usd_to_eur_rate
    elif state.unit == "eur":
        state.converted_value = state.value_to_convert * state.eur_to_usd_rate


if __name__ == "__main__":
    usd_to_eur_rate = 0.9
    eur_to_usd_rate = 1 / usd_to_eur_rate

    value_to_convert = 0
    converted_value = 0
    units = ["usd", "eur"]
    unit = units[0]

    page = Page("converter_page.xprjson")
    Gui(page).run(design=True, title="converter_app", use_reloader=True)
