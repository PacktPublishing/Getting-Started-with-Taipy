import pandas as pd


def add_empty_row(df):
    """Generic function to add an empty row.
    Used by add_row twice

    Args:
        df (pd.DataFrame): df_sales and df_sales_original
    """
    empty_row = pd.DataFrame([[None for _ in df.columns]], columns=df.columns)
    empty_row["Note"] = "New Index"
    df = pd.concat([empty_row, df], axis=0, ignore_index=True)

    return df


def add_row(state, var_name, payload):
    """Callback to add a row from the table command.
        We add a row to both the original dataframe and the working dataframe.
    This way, when we reload data, the changes persist. Both DataFrames have the same index.
    """

    state.df_sales = add_empty_row(state.df_sales)
    state.df_sales_original = add_empty_row(state.df_sales_original)
