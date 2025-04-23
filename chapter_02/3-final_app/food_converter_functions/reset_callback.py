from taipy.gui import notify


def reset(state, id, payload):
    if id != "reset_volume":
        state.grams = 0
        state.ounces = 0
    if id != "reset_weight":
        state.cups = 0
        state.tablespoons = 0
        state.teaspoons = 0
        state.milliliters = 0
    notify(state, notification_type="warning", message="Values set to 0")
