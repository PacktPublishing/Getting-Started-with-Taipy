import taipy.gui.builder as tgb
from taipy.gui import notify

from .scenario_charts import plot_assignments, plot_customer_by_warehouse


def refresh_results_of_scenario(state):
    with state as s:
        s.df_selected_warehouses_dn = s.selected_scenario.df_selected_warehouses
        s.df_selected_warehouses = s.selected_scenario.df_selected_warehouses.read()
        s.df_assignments = s.selected_scenario.df_assignments.read()

        s.total_price = s.selected_scenario.total_price.read()
        s.total_co2 = s.selected_scenario.total_co2.read()
        s.total_cost_per_order = s.selected_scenario.total_cost_per_order.read()
        s.total_co2_per_order = s.selected_scenario.total_co2_per_order.read()


def change_scenario(state):
    with state as s:
        s.optimize = s.selected_scenario.optimization_target.read()
        s.number_of_warehouses = s.selected_scenario.number_of_warehouses.read()
        s.country_list = s.selected_scenario.country_list.read()
        s.co2_per_kilometer = s.selected_scenario.co2_per_km.read()

        refresh_results_of_scenario(s)


def submission_changed(state, submittable, details):
    if details["submission_status"] == "COMPLETED":
        print("Submission completed")
        refresh_results_of_scenario(state)
        notify(state, "s", "Submission completed")
    elif details["submission_status"] == "FAILED":
        notify(state, "error", "Submission failed")


def add_tags_to_scenario(
    scenario,
    optimize,
    number_of_warehouses,
    country_list,
    co2_per_kilometer,
):

    tags = [
        f"Optimization target: {optimize}",
        f"Number of warehouses {number_of_warehouses}",
        f"Price per Km: {scenario.price_per_km.read()}",  # Change this to read from the data node
        f"CO2 per Km: {co2_per_kilometer}",
    ]

    if len(country_list) > 0:
        tags += (f"Fixed countries {country_list}",)

    scenario.tags = tags
    return scenario


def change_settings(state):

    if state.number_of_warehouses != "any":
        if len(state.country_list) > int(state.number_of_warehouses):
            with state as s:
                s.active_scenario = False
                notify(s, "e", "Don't select more countries than warehouses!")
                return

    scenario_date = f"{state.selected_scenario.creation_date.month}-{state.selected_scenario.creation_date.year}"  ### Add this for Answer 4
    if scenario_date in state.kilometer_prices.keys():
        km_cost = state.kilometer_prices.get(scenario_date)
        state.selected_scenario.price_per_km.write(km_cost)
    else:
        # The data node has a default value, we don't need to write it, but we notify the user:
        notify(
            state,
            "w",
            "No Data for kilometer price for selected date - applying default",
        )

    with state as s:
        s.selected_scenario.optimization_target.write(s.optimize)
        s.selected_scenario.number_of_warehouses.write(s.number_of_warehouses)
        s.selected_scenario.country_list.write(s.country_list)

        s.selected_scenario.co2_per_km.write(s.co2_per_kilometer)
        s.selected_scenario = add_tags_to_scenario(
            s.selected_scenario,
            s.optimize,
            s.number_of_warehouses,
            s.country_list,
            s.co2_per_kilometer,
        )
        s.active_scenario = True
        notify(s, "s", "Changed Scenario stettings")


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
                            
- **Number of warehouses**: the number of warehouses to select, must be between 1 and 10. If "any", then the applicatioons selects the optimal warehouses with no more than 10.
- **Fix warehouses**: enable the ability to fix warehouses,
- **Countries to Include**: If selected, the application will assign **at least** one warehouse to each selected country. The application won't let you select more copuntries than warehouses.
- **Price per kilometer**: Total cost per kilometer between a warehouse and a customer. Includes all costs (gas, truck maintainance, wages...) for trips back and forth.
- **CO2 per kilometer**: Total CO2e emissions for transporation of goods between warehouse and customer, for trips back and forth.
        
        """,
                    mode="md",
                )
            with tgb.layout("1 1 1 1"):
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
                    "{co2_per_kilometer}",
                    label="CO2e (Kg) per kilometer",
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
