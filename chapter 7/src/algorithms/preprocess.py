import pandas as pd
import taipy as tp


def calculate_big_numbers(df_sales):
    """
    Calculates key metrics and identifies the best seller from the sales data.

    Args:
        df_sales (pandas.DataFrame): The input DataFrame containing sales data.
                                     It must have the following columns:
                                     - "total_sale": The sales amount for each transaction.
                                     - "quantity": The quantity of items sold.
                                     - "name": The name of the seller or product.

    Returns:
        tuple: A tuple containing the following:
            - Total sales (str): The sum of all sales, formatted with commas and two decimal places.
            - Average sales (str): The average value of sales per invoice, formatted with commas and two decimal places.
            - Best seller (dict): A dictionary containing:
                - "best_seller_name": The name of the seller or product with the highest quantity sold.
                - "best_seller_value": The total quantity sold by the best seller.

    This function performs the following calculations:
    1. **Total Sales:** The total sum of the "total_sale" column.
    2. **Average Sales:** The average of the "total_sale" column.
    3. **Best Seller Identification:** Determines the seller or product with the highest total quantity sold,
       and returns their name and the total quantity.
    """

    total_sales = df_sales["sales"].sum()
    total_sales = f"{total_sales:,.2f}"

    average_sales = df_sales["sales"].mean()
    average_sales = f"{average_sales:,.2f}"

    best_seller = df_sales.groupby("name", observed=True)["items"].sum()
    best_seller_name = best_seller.idxmax()
    best_seller_value = int(best_seller.max())

    best_seller_dict = {
        "best_seller_name": best_seller_name,
        "best_seller_value": best_seller_value,
    }

    return total_sales, average_sales, best_seller_dict


def group_by_dimensions_and_facts(df, dimension_columns, orderby="sales"):
    """
    Groups a DataFrame by specified dimension columns, always aggregating:
        - Count by the "quantity" column.
        - Sum the "total_sale" column.

    Args:
        df (pd.DataFrame): The input DataFrame to group.
        dimension_columns (list of str): List of column names to group by (dimensions).
        orderby (str | list of str): columns name or list of columns to order the DataFrame. Defaults to "sales"


    Returns:
        pd.DataFrame: A grouped DataFrame with the sum of "total_sale" and count of "quantity" for each combination of dimensions.
    """
    df_copy = df.copy()

    # Sum "total_sale" and count "quantity"
    df_grouped = df_copy.groupby(dimension_columns, observed=True).agg(
        sales=("sales", "sum"), items=("items", "count")
    )

    df_grouped = df_grouped.sort_values(by=orderby, ascending=False)

    # Format and return the DataFrame
    df_grouped = df_grouped.round(2)
    df_grouped = df_grouped.reset_index()
    return df_grouped


def group_by_weekday(df_date, extra_col=None):
    """
    Groups the DataFrame by weekday and sorts the result by the weekday order.

    Args:
        df_date (pandas.DataFrame): The input DataFrame containing a 'day' column with weekday abbreviations.
        extra_col (str, optional): An additional column to include in the grouping.

    Returns:
        pandas.DataFrame: A DataFrame with summary information grouped and sorted by weekday.
    """
    # Group by weekday
    if extra_col is None:
        weekday_stats = group_by_dimensions_and_facts(df_date, ["day"])
    else:
        weekday_stats = group_by_dimensions_and_facts(df_date, ["day", extra_col])

    # Define the correct weekday order
    WeekdayOrder = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    # Convert 'day' to a categorical type with the specified order
    weekday_stats["day"] = pd.Categorical(
        weekday_stats["day"], categories=WeekdayOrder, ordered=True
    )

    # Sort the DataFrame by the ordered categorical 'day' column
    weekday_stats = weekday_stats.sort_values(by="day").reset_index(drop=True)

    return weekday_stats
