import taipy.gui.builder as tgb
from algorithms.create_charts import (
    create_customer_heatmap,
    create_product_chart,
    create_time_scatter,
    create_weekday_chart,
)
from algorithms.preprocess import group_by_dimensions_and_facts, group_by_weekday
from pages.sales.partial_sales import (
    # create_partial_sales_customer,
    create_partial_sales_time,
)


# Callbacks
def change_time_charts(state):
    with state as s:
        df_time = s.sales_simplified_node.read()
        is_all = s.time_break_by == "All"

        # Grouping and visualization parameter:
        break_by = None if is_all else s.time_break_by

        # Group and visualize weekday stats
        s.weekday_stats = group_by_weekday(df_time, extra_col=break_by)
        s.weekday_fig = create_weekday_chart(
            s.weekday_stats, y_axis=s.y_axis_time, break_by=break_by
        )

        # Group and visualize date stats
        group_columns = "date" if is_all else ["date", s.time_break_by]
        s.date_stats = group_by_dimensions_and_facts(
            df_time, group_columns, orderby="date"
        )
        s.date_fig = create_time_scatter(
            s.date_stats, y_axis=s.y_axis_time, break_by=break_by
        )

        # Create partial sales time
        create_partial_sales_time(s)


# def change_customer_unit(state):
#     with state as s:
#         # s.customer_heatmap_fig = create_customer_heatmap(
#         #     s.customer_stats, s.z_axis_customer
#         # )
#         create_partial_sales_customer(s)


def change_product_unit(state):
    with state as s:
        s.product_barchart_fig = create_product_chart(s.product_stats, s.y_axis_product)
        # create_partial_sales_customer(s)


with tgb.Page() as sales_page:
    tgb.text("## Historical Sales", mode="md", class_name="color-primary")

    with tgb.layout("1 1 1"):
        with tgb.part("card"):
            tgb.text("## Total Sales ", mode="md", class_name="color-secondary")
            tgb.text(
                "### $ {total_sales}",
                mode="md",
                class_name="color-primary",
            )
        with tgb.part("card"):
            tgb.text("## Average Sale ", mode="md", class_name="color-secondary")
            tgb.text(
                "### $ {average_sales}",
                mode="md",
                class_name="color-primary",
            )
        with tgb.part("card"):
            tgb.text(
                "## MVP: {best_seller_dict['best_seller_name']}",
                mode="md",
                class_name="color-secondary",
            )
            tgb.text(
                "### {best_seller_dict['best_seller_value']} units",
                mode="md",
                class_name="color-primary",
            )

    with tgb.expandable(
        "Sales over Time",
        class_name="color-primary",
        expanded=False,
    ):
        with tgb.layout("1 1"):
            tgb.toggle(
                value="{time_break_by}",
                lov=["All", "gender", "generation", "type", "color", "style"],
                label="Break values by",
                on_change=change_time_charts,
            )
            tgb.toggle(
                value="{y_axis_time}",
                lov=["sales", "items"],
                label="Select units",
                on_change=change_time_charts,
            )
        tgb.part(
            partial="{partial_sales_time}",
        )

    with tgb.expandable(
        "Sales by Customer",
        class_name="color-primary",
        expanded=False,
    ):
        with tgb.layout("1 1"):
            with tgb.part():
                tgb.toggle(
                    value="{z_axis_customer}",
                    lov=["sales", "items"],
                    label="Select units",
                    # on_change=change_customer_unit, # This is not useful now because
                    # the heatmap is bound to the z_axis_customer. See below
                )
                tgb.chart(
                    figure=lambda customer_stats, z_axis_customer: create_customer_heatmap(
                        customer_stats, z_axis_customer
                    )
                )

            tgb.table(
                "{df_sales_customer}",
                page_size=15,
                filter=True,
                cell_class_name__items=lambda _: "col-number",
                cell_class_name__sales=lambda _: "col-number",
            )

    with tgb.expandable(
        "Sales by Product",
        class_name="color-primary",
        expanded=False,
    ):
        with tgb.layout("1 1"):
            with tgb.part():
                tgb.toggle(
                    value="{y_axis_product}",
                    lov=["sales", "items"],
                    label="Select units",
                    on_change=change_product_unit,
                )
                tgb.part(
                    partial="{partial_sales_product}",
                )

            tgb.table(
                "{df_sales_product}",
                page_size=15,
                filter=True,
                cell_class_name__items=lambda _: "col-number",
                cell_class_name__sales=lambda _: "col-number",
            )

    with tgb.expandable(
        "All Sales",
        class_name="color-primary",
        expanded=False,
    ):
        tgb.table(
            data="{df_sales}",
            page_size=25,
            filter=True,
            downloadable=True,
            cell_class_name__unit_price=lambda _: "col-number",
            cell_class_name__items=lambda _: "col-number",
            cell_class_name__sales=lambda _: "col-number",
        )
