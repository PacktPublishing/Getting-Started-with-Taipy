def change_weight(state, var_name, value):
    if var_name == "grams":  # Grams to Ounces
        state.ounces = round(value / 28.35, 2)
    else:  # Ounces to Grams
        state.grams = round(value * 28.35, 2)
