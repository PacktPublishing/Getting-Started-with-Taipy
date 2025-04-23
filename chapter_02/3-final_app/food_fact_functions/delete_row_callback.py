def delete_row(state, var_name, payload):
    index = payload["index"]
    state.df_sales = state.df_sales.drop(index=index)
    state.df_sales_original = state.df_sales_original.drop(index=index)
