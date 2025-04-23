def change_volume(state, var_name, value):
    if var_name == "cups":
        # state.tablespoons = round(value * 16, 2)
        state.tablespoons = value * 16
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
