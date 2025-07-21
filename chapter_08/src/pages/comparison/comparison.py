from pages.scenario.scenario_charts import plot_assignments

import taipy.gui.builder as tgb

scenario_1 = None
scenario_2 = None


with tgb.Page() as comparison_page:

    tgb.text("# **Compare** Scenarios", mode="md")
    tgb.html("hr")
    with tgb.part(class_name="content-block"):
        with tgb.layout("1 1", columns__mobile="1"):
            with tgb.part(
                class_name="vertical-line-border",
            ):
                tgb.text(
                    lambda scenario_1: f"#### Scenario 1 **(Reference)**: {scenario_1.name if scenario_1 else 'Not selected yet'}",
                    mode="md",
                )
                tgb.scenario_selector("{scenario_1}", show_add_button=False)

                with tgb.layout("1 1"):
                    tgb.metric(
                        value=lambda scenario_1: (
                            scenario_1.total_price.read() if scenario_1 else None
                        ),
                        title="Scenario 1's Total Price",
                        format=" €",
                        type="none",
                        hover_text="Scenario 1 - Total carbon footprint.",
                        class_name="mb2 mt2",
                    )
                    tgb.metric(
                        value=lambda scenario_1: (
                            scenario_1.total_co2.read() if scenario_1 else None
                        ),
                        title="Scenario 1's Total CO2e",
                        format=" T",
                        type="none",
                        hover_text="Scenario 1 - Total carbon footprint.",
                        class_name="mb2 mt2",
                    )
                tgb.chart(
                    figure=lambda scenario_1: plot_assignments(
                        scenario_1.df_assignments.read() if scenario_1 else None
                    )
                )
                with tgb.part():
                    tgb.text("### Scenario 1's **Warehouses**", mode="md")
                    tgb.data_node(
                        lambda scenario_1: (
                            scenario_1.df_selected_warehouses if scenario_1 else None
                        ),
                        expanded=False,
                        file_download=True,
                    )
            with tgb.part():
                tgb.text(
                    lambda scenario_2: f"#### Scenario 2 **(Compare with)**: {scenario_2.name if scenario_2 else 'Not selected yet'}",
                    mode="md",
                )
                tgb.scenario_selector("{scenario_2}", show_add_button=False)
                with tgb.layout("1 1"):
                    tgb.metric(
                        value="{scenario_2.total_price.read()}",
                        title="Scenario 2's Total Price",
                        format=" €",
                        type="none",
                        hover_text="Scenario 2 - Total carbon footprint.",
                        class_name="mb2 mt2",
                    )
                    tgb.metric(
                        value="{scenario_2.total_co2.read()}",
                        title="Scenario 2's Total CO2e",
                        format=" T",
                        type="none",
                        hover_text="Scenario 2 - Total carbon footprint.",
                        class_name="mb2 mt2",
                    )
                tgb.chart(
                    figure=lambda scenario_2: plot_assignments(
                        scenario_2.df_assignments.read() if scenario_2 else None
                    )
                )
                with tgb.part():
                    tgb.text("### Scenario 2's **Warehouses**", mode="md")
                    tgb.data_node(
                        lambda scenario_2: (
                            scenario_2.df_selected_warehouses if scenario_2 else None
                        ),
                        expanded=False,
                        file_download=True,
                    )
    tgb.text("## **Scenario 1** compared to Scenario 2:", mode="md")
    tgb.html("hr")
    with tgb.part(class_name="content-block"):
        with tgb.layout("1 1 1 1", columns__mobile="1"):
            tgb.metric(
                value=lambda scenario_1, scenario_2: (
                    scenario_1.total_price.read() if scenario_1 and scenario_2 else None
                ),
                delta=lambda scenario_1, scenario_2: (
                    scenario_1.total_price.read() - scenario_2.total_price.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                type="none",
                delta_color="invert",
                format=" €",
                title="Comparison - Total Cost",
                hover_text="Cost comparison of both solutions.",
                class_name="mb1 mt1 pb1",
            )
            tgb.metric(
                value=lambda scenario_1, scenario_2: (
                    scenario_1.total_co2.read() if scenario_1 and scenario_2 else None
                ),
                delta=lambda scenario_1, scenario_2: (
                    scenario_1.total_co2.read() - scenario_2.total_co2.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                type="none",
                delta_color="invert",
                format=" T",
                title="Comparison - Total CO2e",
                hover_text="CO2 emission comparison of both solutions.",
                class_name="mb1 mt1 pb1",
            )
            tgb.metric(
                lambda scenario_1, scenario_2: (
                    scenario_1.total_cost_per_order.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                delta=lambda scenario_1, scenario_2: (
                    scenario_1.total_cost_per_order.read()
                    - scenario_2.total_cost_per_order.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                delta_color="invert",
                type="linear",
                max=6_000,
                threshold=lambda scenario_1, scenario_2: (
                    scenario_2.total_cost_per_order.read()
                    if scenario_1 and scenario_2
                    else 1
                ),
                format=" €",
                title="Avg cost/order",
                hover_text="Estimated average transportation cost per truck shipping.",
                class_name="mb2 mt2 pb1",
                color_map={
                    0: "#90EE90",
                    2_000: "#FF6347",
                },
                bar_color="#003399",
            )
            tgb.metric(
                lambda scenario_1, scenario_2: (
                    scenario_1.total_co2_per_order.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                delta=lambda scenario_1, scenario_2: (
                    scenario_1.total_co2_per_order.read()
                    - scenario_2.total_co2_per_order.read()
                    if scenario_1 and scenario_2
                    else None
                ),
                delta_color="invert",
                type="linear",
                max=3_000,
                threshold=lambda scenario_1, scenario_2: (
                    scenario_2.total_co2_per_order.read()
                    if scenario_1 and scenario_2
                    else 1
                ),
                format=" Kg",
                title="Avg CO2e/order",
                hover_text="Estimated average CO2 emissions per truck shipping.",
                class_name="mb2 mt2 pb1",
                color_map={
                    0: "#90EE90",
                    1_000: "#FF6347",
                },
                bar_color="#003399",
            )
