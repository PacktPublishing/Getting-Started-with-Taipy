import taipy.gui.builder as tgb

with tgb.Page() as dynamic_chart_page:
    tgb.text(
        "## Dynamic Charts",
        mode="md",
    )

    tgb.table(data="{df_parish_info}")
    tgb.selector(
        "{accommodation}",
        lov="{accommodation_type}",
        dropdown=True,
        class_name="fullwidth",
    )

    tgb.part(content="{JsChartClass(df_parish_info, accommodation)}", height="500px")
