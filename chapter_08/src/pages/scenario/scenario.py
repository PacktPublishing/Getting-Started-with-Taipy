import taipy.gui.builder as tgb
from taipy.gui import notify

from .scenario_charts import plot_assignments, plot_customer_by_warehouse


def refresh_results_of_scenario(state):
    """This function use getattr and setattr to avoid long repetitions
    in the if/else statement"""
    bound_variables_to_write = [
        "df_selected_warehouses",
        "df_assignments",
        "total_price",
        "total_co2",
        "total_cost_per_order",
        "total_co2_per_order",
    ]
    with state as s:
        s.df_selected_warehouses_dn = s.selected_scenario.df_selected_warehouses
        if s.selected_scenario.total_price.is_ready_for_reading:
            for bound_variable in bound_variables_to_write:
                setattr(
                    s,
                    bound_variable,
                    getattr(s.selected_scenario, bound_variable).read(),
                )
        else:
            for bound_variable in bound_variables_to_write:
                setattr(s, bound_variable, None)


def change_scenario(state):
    with state as s:
        s.optimize = s.selected_scenario.optimization_target.read()
        s.number_of_warehouses = s.selected_scenario.number_of_warehouses.read()
        s.country_list = s.selected_scenario.country_list.read()
        s.price_per_km = s.selected_scenario.price_per_km.read()
        s.co2_per_km = s.selected_scenario.co2_per_km.read()
        refresh_results_of_scenario(s)


def submission_changed(state, submittable, details):
    with state as s:
        if details["submission_status"] == "COMPLETED":
            print("Submission completed")
            refresh_results_of_scenario(s)
            notify(s, "s", "Submission completed")
        elif details["submission_status"] == "FAILED":
            notify(s, "error", "Submission failed")


def add_tags_to_scenario(
    scenario,
    optimize,
    number_of_warehouses,
    country_list,
    price_per_km,
    co2_per_km,
):

    tags = [
        f"Optimization target: {optimize}",
        f"Number of warehouses {number_of_warehouses}",
        f"Price per Km: {price_per_km}",
        f"CO2 per Km: {co2_per_km}",
    ]

    if len(country_list) > 0:
        tags += (f"Fixed countries {country_list}",)

    scenario.tags = tags
    return scenario


def change_settings(state):
    with state as s:
        if state.number_of_warehouses != "any":
            if len(state.country_list) > int(state.number_of_warehouses):
                s.active_scenario = False
                notify(s, "e", "Don't select more countries than warehouses!")
                return
    with state as s:
        s.selected_scenario.optimization_target.write(s.optimize)
        s.selected_scenario.number_of_warehouses.write(s.number_of_warehouses)
        s.selected_scenario.country_list.write(s.country_list)
        s.selected_scenario.price_per_km.write(s.price_per_km)
        s.selected_scenario.co2_per_km.write(s.co2_per_km)
        s.selected_scenario = add_tags_to_scenario(
            s.selected_scenario,
            s.optimize,
            s.number_of_warehouses,
            s.country_list,
            s.price_per_km,
            s.co2_per_km,
        )
        s.active_scenario = True
        notify(s, "s", "Changed Scenario settings")


def deactivate_scenario(state):
    with state as s:
        s.active_scenario = False
        notify(s, "i", "Add settings to new Scenario")


with tgb.Page() as scenario_page:

    with tgb.layout("1 4", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.text("**Create** and select scenarios", mode="md")
            tgb.scenario_selector(
                "{selected_scenario}",
                on_change=change_scenario,
                on_creation=deactivate_scenario,
            )

        with tgb.part("main"):
            tgb.text("# **Create** Scenario", mode="md")
            tgb.html("hr")

            with tgb.expandable("Instructions", expanded=False):

                tgb.text(
                    """Select scenario's **parameters** and constraints:
                            
- **Number of warehouses**: The number of warehouses to select; must be between 1 and 10. If "any", then the application selects the optimal warehouses with no more than 10.
- **Fix warehouses**: Enable the ability to fix warehouses.
- **Countries to include**: If selected, the application will assign **at least** one warehouse to each selected country. The application won't let you select more countries than warehouses.
- **Price per km**: Total cost per kilometer between a warehouse and a customer. Includes all costs (gas, truck maintenance, wages...) for trips back and forth.
- **CO2 per km**: Total CO2e emissions for transportation of goods between warehouse and customer, for trips back and forth.
""",
                    mode="md",
                )
            with tgb.layout("1 1 1 1 1"):
                tgb.toggle("{optimize}", label="Optimize", lov=["price", "co2"])
                tgb.selector(
                    "{number_of_warehouses}",
                    lov=["any", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    dropdown=True,
                    label="Numbre of warehouses",
                )
                tgb.selector(
                    "{country_list}",
                    lov="{all_countries}",
                    label="Countries to Include",
                    multiple=True,
                    dropdown=True,
                )
                tgb.number(
                    "{price_per_km}",
                    label="price per km",
                    min=1,
                    max=10,
                    step=0.1,
                )
                tgb.number(
                    "{co2_per_km}",
                    label="CO2e (Kg) per km",
                    min=1,
                    max=10,
                    step=0.1,
                )

            tgb.button(
                "Change Settings",
                on_action=change_settings,
                class_name="fullwidth",
            )

            tgb.scenario(
                "{selected_scenario}",
                show_sequences=False,
                on_submission_change=submission_changed,
                active="{active_scenario}",
            )

            tgb.text("### **Scenario** results", mode="md")
            tgb.data_node(
                "{df_selected_warehouses_dn}", show_history=False, expanded=False
            )

            with tgb.layout("1 1 1 1", columns__mobile="1"):
                tgb.metric(
                    value="{total_price}",
                    title="Scenario's Total Price",
                    format=" €",
                    type="none",
                    hover_text="Estimated total carbon footprint.",
                    class_name="mb2 mt2",
                )
                tgb.metric(
                    value="{total_co2}",
                    title="Scenario's Total CO2e",
                    format=" T",
                    type="none",
                    hover_text="Estimated total carbon footprint.",
                    class_name="mb2 mt2",
                )
                tgb.metric(
                    value="{total_cost_per_order}",
                    max=6_000,
                    threshold=2_000,
                    format=" €",
                    title="Avg cost/order",
                    hover_text="Estimated average transportation cost per truck shipping.",
                    class_name="mb2 mt2 pb1",
                )
                tgb.metric(
                    value="{total_co2_per_order}",
                    max=3_000,
                    threshold=1_000,
                    format=" Kg",
                    title="Avg CO2e emissions/order",
                    hover_text="Estimated average CO2e emissions per truck shipping.",
                    class_name="mb2 mt2 pb1",
                )

            tgb.chart(figure=lambda df_assignments: plot_assignments(df_assignments))

            tgb.chart(
                figure=lambda df_assignments: plot_customer_by_warehouse(df_assignments)
            )
            with tgb.layout("1 1"):
                tgb.chart(
                    "{df_selected_warehouses}",
                    type="bar",
                    x="warehouse",
                    y="scenario_cost",
                    title="Total cost by selected warehouse",
                    color="#003399",
                )
                tgb.chart(
                    "{df_selected_warehouses}",
                    type="bar",
                    x="warehouse",
                    y="scenario_co2_tons",
                    title="Total CO2e emissions by selected warehouse",
                    color="#003399",
                )
