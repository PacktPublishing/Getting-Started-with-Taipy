import pandas as pd
import us


def clean_sales_data(sales_csv_file):
    """Cleans a CSV file containing sales data.
    * Remove the fisrt 2 and last 3 rows (not data)
    * Rename long columns
    * Transform numeric columns to float (CSV has spaces between numbers)
    * Add US State codes for plotting geographical data
    * A a "Note" column for users to add data

    Args:
        sales_csv_file: The path to the CSV file.

    Returns:
        A cleaned pandas DataFrame.
    """

    df_sales = pd.read_csv(sales_csv_file, skiprows=2).iloc[:-3]

    numeric_columns = [
        "Constant-dollar sales (1988=100) - FAH",
        "Constant-dollar sales (1988=100) - FAFH",
        "Total constant-dollar food sales",
        "Nominal sales - FAH",
        "Nominal sales - FAFH",
        "Total nominal food sales",
    ]

    for metric in numeric_columns:
        df_sales[metric] = df_sales[metric].astype(str).str.replace(" ", "")
        df_sales[metric] = pd.to_numeric(df_sales[metric], errors="coerce")

    df_sales.rename(
        columns={
            "Nominal sales - FAH": "FAH_nominal",
            "Nominal sales - FAFH": "FAFH_nominal",
            "Total nominal food sales": "Total_nominal",
            "Constant-dollar sales (1988=100) - FAH": "FAH_constant",
            "Constant-dollar sales (1988=100) - FAFH": "FAFH_constant",
            "Total constant-dollar food sales": "Total_constant",
        },
        inplace=True,
    )

    # Add a new column for US state codes
    df_sales["State_Code"] = df_sales["State"].apply(
        lambda x: "DC" if x == "District of Columbia" else us.states.lookup(x).abbr
    )

    # Add an empty "Note" column
    df_sales["Note"] = ""

    return df_sales


def update_df_sales(df_sales, adjust_inflation=False):
    """Updates a DataFrame with sales data. It selects the "constant" columns
    to display values adjusted for inflation, or "nominal" otherwise (default)

    Args:
        df_sales: The DataFrame containing sales data.
        adjust_inflation: Whether to adjust for inflation (default: False).

    Returns:
        A modified DataFrame with renamed columns.
    """

    df_sales_cp = df_sales.copy()

    nominal_columns = ["FAH_nominal", "FAFH_nominal", "Total_nominal"]
    contant_columns = ["FAH_constant", "FAFH_constant", "Total_constant"]
    # For renaming:
    metric_columns = ["FAH", "FAFH", "Total"]

    if adjust_inflation:  # rename constant, drop nominal
        df_sales_cp.drop(
            columns=nominal_columns,
            inplace=True,
        )
        rename_dict = dict(zip(contant_columns, metric_columns))

    else:  # rename nominal, drop constant
        df_sales_cp.drop(
            columns=contant_columns,
            inplace=True,
        )
        rename_dict = dict(zip(nominal_columns, metric_columns))

    df_sales_cp.rename(
        columns=rename_dict,
        inplace=True,
    )

    return df_sales_cp
