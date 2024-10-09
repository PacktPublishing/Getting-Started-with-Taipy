def select_subset(df_auto_mpg, columns):
    """Selects a subset of the `df_auto_mpg` DataFrame, including the 'mpg' column and the specified columns.

    Args:
        df_auto_mpg (pandas.DataFrame): The original DataFrame containing car data.
        columns (list[str]): A list of column names to include in the subset.

    Returns:
        pandas.DataFrame: A new DataFrame containing only the 'mpg' and specified columns.

    Raises:
        ValueError: If any of the specified column names are not valid.
    """

    valid_columns = [
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model year",
        "origin",
        "car name",
    ]

    for column in columns:
        if column not in valid_columns:
            raise ValueError(f"Invalid column name: {column}")

    dataframe_columns = ["mpg"] + columns
    df_auto_mpg_filtered = df_auto_mpg[dataframe_columns]
    return df_auto_mpg_filtered
