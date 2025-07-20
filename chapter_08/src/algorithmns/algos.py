import pandas as pd
import pulp

#### Optimization functions ####


def initialize_problem():
    """
    Initialize a PuLP minimization problem.
    """
    return pulp.LpProblem("Warehouse_Selection", pulp.LpMinimize)


def define_variables(df_warehouses, df_customers):
    """
    Creates binary decision variables for warehouse selection and customer assignment.
    """
    warehouses = df_warehouses.index.tolist()
    customers = df_customers.index.tolist()

    warehouse_var = pulp.LpVariable.dicts("Warehouse", warehouses, cat="Binary")
    assignment_var = pulp.LpVariable.dicts(
        "Assignment", [(w, c) for w in warehouses for c in customers], cat="Binary"
    )
    return warehouse_var, assignment_var


def _objective_total(
    assignment_var,
    warehouse_var,
    df_warehouses,
    df_customers,
    distance_matrix,
    transport_unit_cost,
    warehouse_cost_column,
    warehouse_cost_multiplier=1,
):
    """
    Generic objective builder for either price or CO₂.
    """
    warehouses = df_warehouses.index.tolist()
    customers = df_customers.index.tolist()

    transport_total = pulp.lpSum(
        assignment_var[(w, c)]
        * distance_matrix.at[w, c]
        * transport_unit_cost
        * df_customers.at[c, "yearly_orders"]
        for w in warehouses
        for c in customers
    )

    warehouse_total = pulp.lpSum(
        warehouse_var[w]
        * df_warehouses.at[w, warehouse_cost_column]
        * warehouse_cost_multiplier
        for w in warehouses
    )

    return transport_total + warehouse_total


def set_objective_function(
    prob,
    assignment_var,
    warehouse_var,
    df_warehouses,
    df_customers,
    distance_matrix,
    optimize,
    price_per_km=4,
    co2_per_km=2,
):
    """
    Adds the selected objective (price or co2) to the optimization problem.
    """
    if optimize == "price":
        prob += _objective_total(
            assignment_var,
            warehouse_var,
            df_warehouses,
            df_customers,
            distance_matrix,
            transport_unit_cost=price_per_km,
            warehouse_cost_column="yearly_cost",
        )
    else:
        prob += _objective_total(
            assignment_var,
            warehouse_var,
            df_warehouses,
            df_customers,
            distance_matrix,
            transport_unit_cost=co2_per_km,
            warehouse_cost_column="yearly_co2_tons",
            warehouse_cost_multiplier=1000,  # Convert tons to kg
        )


def add_constraints(
    prob,
    assignment_var,
    warehouse_var,
    df_warehouses,
    df_customers,
    number_of_warehouses,
    country_list=None,
):
    """
    Adds problem constraints.
    """
    warehouses = df_warehouses.index.tolist()
    customers = df_customers.index.tolist()

    # 1. Each customer is assigned to exactly one warehouse
    for c in customers:
        prob += pulp.lpSum(assignment_var[(w, c)] for w in warehouses) == 1

    # 2. Customers can only be assigned to selected warehouses
    for w in warehouses:
        for c in customers:
            prob += assignment_var[(w, c)] <= warehouse_var[w]

    # 3. Limit number of warehouses
    if number_of_warehouses != "any":
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) == int(
            number_of_warehouses
        )
    else:
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) >= 1
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) <= 10

    # 4. Country constraints (optional)
    if country_list:
        for country in country_list:
            wh_in_country = df_warehouses[
                df_warehouses["country"] == country
            ].index.tolist()
            prob += pulp.lpSum(warehouse_var[w] for w in wh_in_country) >= 1


def extract_results(
    warehouse_var,
    assignment_var,
    df_warehouses,
    df_customers,
    distance_matrix,
    price_per_km=4,
    co2_per_km=2,
):
    """
    Extracts the results from the solved problem and formats them.
    """
    selected_warehouses = [
        w for w in df_warehouses.index if pulp.value(warehouse_var[w]) == 1
    ]
    customers = df_customers.index.tolist()

    assignments = []
    scenario_costs = []
    scenario_co2s = []
    scenario_orders = []

    for w in selected_warehouses:
        yearly_cost = df_warehouses.at[w, "yearly_cost"]
        yearly_co2_tons = df_warehouses.at[w, "yearly_co2_tons"]
        total_transport_cost = 0
        total_transport_co2 = 0
        warehouse_orders = 0

        for c in customers:
            if pulp.value(assignment_var[(w, c)]) == 1:
                distance = distance_matrix.at[w, c]
                orders = df_customers.at[c, "yearly_orders"]

                total_transport_cost += distance * price_per_km * orders
                total_transport_co2 += distance * co2_per_km * orders
                warehouse_orders += orders

                assignments.append(
                    {
                        "warehouse": df_warehouses.at[w, "warehouse"],
                        "warehouse_lat": df_warehouses.at[w, "latitude"],
                        "warehouse_lon": df_warehouses.at[w, "longitude"],
                        "customer": df_customers.at[c, "company_name"],
                        "customer_lat": df_customers.at[c, "latitude"],
                        "customer_lon": df_customers.at[c, "longitude"],
                        "distance_km": distance,
                        "orders": orders,
                        "total_cost": int(distance * price_per_km * orders),
                        "total_co2_kg": int(distance * co2_per_km * orders),
                    }
                )

        scenario_costs.append(int(yearly_cost + total_transport_cost))
        scenario_co2s.append(int(yearly_co2_tons + total_transport_co2 / 1000))
        scenario_orders.append(warehouse_orders)

    df_selected = df_warehouses.loc[selected_warehouses].copy()
    df_selected["scenario_cost"] = scenario_costs
    df_selected["scenario_co2_tons"] = scenario_co2s
    df_selected["scenario_orders"] = scenario_orders
    df_assignments = pd.DataFrame(assignments)

    return df_selected, df_assignments


def create_pulp_model(
    df_warehouses,
    df_customers,
    distance_matrix,
    optimize="price",
    number_of_warehouses="any",
    country_list=None,
    price_per_km=4,
    co2_per_km=2,
):
    """
    Creates and solves the warehouse optimization problem using PuLP.
    """
    df_warehouses = df_warehouses.copy()
    df_customers = df_customers.copy()
    df_warehouses["id"] = df_warehouses.index
    df_customers["id"] = df_customers.index

    prob = initialize_problem()
    warehouse_var, assignment_var = define_variables(df_warehouses, df_customers)
    set_objective_function(
        prob,
        assignment_var,
        warehouse_var,
        df_warehouses,
        df_customers,
        distance_matrix,
        optimize,
        price_per_km,
        co2_per_km,
    )
    add_constraints(
        prob,
        assignment_var,
        warehouse_var,
        df_warehouses,
        df_customers,
        number_of_warehouses,
        country_list,
    )
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    return extract_results(
        warehouse_var,
        assignment_var,
        df_warehouses,
        df_customers,
        distance_matrix,
        price_per_km,
        co2_per_km,
    )


#### Optimization functions END ####


def calculate_total_numbers(df_scenario):
    """
    Returns the total price and CO2 emissions for a Scenario (for all warehouses).
    Returns total amounts and total amount per truck order.
    """
    total_cost = df_scenario["scenario_cost"].sum()
    total_co2 = df_scenario["scenario_co2_tons"].sum()

    total_orders = df_scenario["scenario_orders"].sum()
    price_per_order = total_cost / total_orders
    co2_per_order = total_co2 * 1000 / total_orders

    return int(total_cost), int(total_co2), int(price_per_order), int(co2_per_order)
