import taipy.gui.builder as tgb

from .create_charts import plot_customers_warehouses

with tgb.Page() as analysis_page:

    tgb.text("# **Available** Warehouses", mode="md")
    tgb.html("hr")
    with tgb.part(class_name="content-block"):
        with tgb.expandable("All Locations", expanded=False):
            with tgb.layout("1 1"):
                tgb.table(
                    "{df_warehouses}",
                    page_size=20,
                    columns={
                        "warehouse": {},
                        "country": {},
                        "city": {},
                        "latitude": {"format": "%.02f"},
                        "longitude": {"format": "%.02f"},
                        "yearly_cost": {"format": "%,.0f"},
                        "yearly_co2_tons": {"format": "%,.0f"},
                    },
                    cell_class_name__latitude=lambda _: "col-number",
                    cell_class_name__longitude=lambda _: "col-number",
                    cell_class_name__yearly_cost=lambda _: "col-number",
                    cell_class_name__yearly_co2_tons=lambda _: "col-number",
                )
                tgb.table(
                    "{df_customers}",
                    page_size=20,
                    columns={
                        "country": {},
                        "city": {},
                        "latitude": {"format": "%.02f"},
                        "longitude": {"format": "%.02f"},
                        "company_name": {},
                        "yearly_orders": {"format": "%,.0f"},
                    },
                    cell_class_name__yearly_orders=lambda _: "col-number",
                    cell_class_name__latitude=lambda _: "col-number",
                    cell_class_name__longitude=lambda _: "col-number",
                )

        tgb.chart(
            figure=lambda df_customers, df_warehouses: plot_customers_warehouses(
                df_customers, df_warehouses
            ),
            height="600px",
            class_name="m1",
        )
        with tgb.layout("1 1"):
            tgb.chart(
                "{df_warehouses}",
                type="bar",
                x="city",
                y="yearly_cost",
                title="Potential Warehouses and yearly rent",
            )
            tgb.chart(
                "{df_customers}",
                type="bar",
                x="company_name",
                y="yearly_orders",
                title="Orders by client",
            )
