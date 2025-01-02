import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from algorithms.create_charts import (
    create_customer_heatmap,
    create_product_chart,
    create_time_scatter,
    create_weekday_chart,
)
from algorithms.preprocess import (
    calculate_big_numbers,
    group_by_dimensions_and_facts,
    group_by_weekday,
)
from configuration.config import (
    sales_customer_node_config,
    sales_node_config,
    sales_product_node_config,
    sales_simplified_node_config,
)
from pages.forecast import forecast_page
from pages.sales.partial_sales import (
    create_partial_sales_customer,
    create_partial_sales_product,
    create_partial_sales_time,
)
from pages.sales.sales import sales_page
from taipy import Orchestrator
from taipy.gui import Gui

with tgb.Page() as root_page:
    tgb.toggle(theme=True)

    tgb.text("# Company Sales Forecast App 📈", mode="md", class_name="color-primary")
    tgb.navbar()
    tgb.content()

sales_forecast_pages = {
    "/": root_page,
    "historical_data": sales_page,
    "forecast": forecast_page,
}

stylekit = {
    "color_primary": "#66C2A5",  # metallic medium sea green
    "color_secondary": "#A9A9A9",  # metallic dark grey (dark gray)
}

##################
## Partials     ##
##################


def on_init(state):
    create_partial_sales_time(state)
    create_partial_sales_customer(state)
    create_partial_sales_product(state)


if __name__ == "__main__":
    # Values for selectors
    time_break_by = "All"
    y_axis_time = "sales"
    z_axis_customer = "sales"
    y_axis_product = "sales"
    forecast_target = "sales"
    gender_forecast = "All"
    generation_forecast = "All"
    product_forecast = "All"
    selected_scenario = None
    # For forecast:
    scenario_name = ""
    prediction_number_days = 30
    show_predictions = False
    df_results = pd.DataFrame(columns=["date", "forecast", "conf_min", "conf_max"])
    selected_scenario_name = ""
    forecast_fig = None
    total_forecast_value = 0
    min_forecast_value = 0
    max_forecast_value = 0

    orchestrator = Orchestrator()
    orchestrator.run()

    # Create Data Nodes
    sales_node = tp.create_global_data_node(sales_node_config)
    df_sales = sales_node.read()

    sales_customer_node = tp.create_global_data_node(sales_customer_node_config)
    df_sales_customer = sales_customer_node.read()

    sales_product_node = tp.create_global_data_node(sales_product_node_config)
    df_sales_product = sales_product_node.read()

    sales_simplified_node = tp.create_global_data_node(sales_simplified_node_config)
    df_sales_simplified = sales_simplified_node.read()

    # Start the agregated DataFrames for the dashboard
    weekday_stats = group_by_weekday(df_sales_simplified)
    date_stats = group_by_dimensions_and_facts(
        df_sales_simplified, "date", orderby="date"
    )
    customer_stats = group_by_dimensions_and_facts(
        df_sales_simplified, ["gender", "generation"]
    )
    product_stats = group_by_dimensions_and_facts(
        df_sales_simplified, ["type", "color"]
    )

    # Big numbers
    total_sales, average_sales, best_seller_dict = calculate_big_numbers(df_sales)

    # Custom charts
    weekday_fig = create_weekday_chart(weekday_stats, y_axis_time)
    date_fig = create_time_scatter(date_stats, y_axis_time)
    customer_heatmap_fig = create_customer_heatmap(customer_stats, z_axis_customer)
    product_barchart_fig = create_product_chart(product_stats, y_axis_product)

    # Create app
    sales_forecast_gui = Gui(pages=sales_forecast_pages, css_file="./css/main.css")

    # Add partials:
    partial_sales_time = sales_forecast_gui.add_partial("")
    partial_sales_customer = sales_forecast_gui.add_partial("")
    partial_sales_product = sales_forecast_gui.add_partial("")

    sales_forecast_gui.run(
        # use_reloader=True, # For development
        title="Sales Forecast",
        favicon="./images/favicon.ico",
        stylekit=stylekit,
    )
