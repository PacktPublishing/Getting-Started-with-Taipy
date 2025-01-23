import taipy.gui.builder as tgb


def create_partial_sales_time(state):
    with tgb.Page() as link_part:
        with tgb.layout("1 1"):
            tgb.chart(figure="{weekday_fig}")
            tgb.chart(figure="{date_fig}")
    state.partial_sales_time.update_content(state, link_part)


# def create_partial_sales_customer(state):
#     with tgb.Page() as link_part:
#         tgb.chart(figure="{create_customer_heatmap(customer_stats, z_axis_customer)}")
#     state.partial_sales_customer.update_content(state, link_part)


def create_partial_sales_product(state):
    with tgb.Page() as link_part:
        tgb.chart(figure="{product_barchart_fig}")
    state.partial_sales_product.update_content(state, link_part)
