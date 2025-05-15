def add_note(df, index, col, note):
    df_note = df.copy()
    df_note.loc[index, col] = note

    return df_note


def edit_note(state, var_name, payload):
    if payload["col"] == "Note":
        state.df_sales = add_note(
            state.df_sales, payload["index"], payload["col"], payload["value"]
        )

        state.df_sales_original = add_note(
            state.df_sales_original, payload["index"], payload["col"], payload["value"]
        )
