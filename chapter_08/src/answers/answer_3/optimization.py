import pandas as pd
import pulp

from .problem_data import ProblemData


def _initialize_problem():
    """
    Initialize a PuLP minimization problem.
    """
    return pulp.LpProblem("Warehouse_Selection", pulp.LpMinimize)


def _define_variables(data: ProblemData):
    warehouses = data.df_warehouses.index.tolist()
    customers = data.df_customers.index.tolist()
    warehouse_var = pulp.LpVariable.dicts("Warehouse", warehouses, cat="Binary")
    assignment_var = pulp.LpVariable.dicts(
        "Assignment", [(w, c) for w in warehouses for c in customers], cat="Binary"
    )
    return warehouse_var, assignment_var


def _compute_transport_cost_term(assignment_var, data: ProblemData):
    """
    Computes the total transport cost across all customer-warehouse assignments.

    Cost is calculated as:
    distance * price_per_km * yearly_orders
    """
    return pulp.lpSum(
        assignment_var[(w, c)]
        * data.distance_matrix.at[w, c]
        * data.price_per_km
        * data.df_customers.at[c, "yearly_orders"]
        for w in data.df_warehouses.index
        for c in data.df_customers.index
    )


def _compute_transport_co2_term(assignment_var, data: ProblemData):
    """
    Computes total CO₂ emissions from transport.

    Emissions are calculated as:
    distance * co2_per_km * yearly_orders
    """
    return pulp.lpSum(
        assignment_var[(w, c)]
        * data.distance_matrix.at[w, c]
        * data.co2_per_km
        * data.df_customers.at[c, "yearly_orders"]
        for w in data.df_warehouses.index
        for c in data.df_customers.index
    )


def _compute_warehouse_cost_term(
    warehouse_var, data: ProblemData, column, multiplier=1
):
    """
    Computes fixed warehouse costs or emissions depending on the specified column.

    Args:
        warehouse_var: Decision variable dict for warehouses
        data: ProblemData instance
        column: Column name to read values from (e.g. 'yearly_cost', 'yearly_co2_tons')
        multiplier: Optional multiplier (e.g. for unit conversions like tons -> kg)

    Returns:
        Total cost or emission expression for all selected warehouses
    """
    return pulp.lpSum(
        warehouse_var[w] * data.df_warehouses.at[w, column] * multiplier
        for w in data.df_warehouses.index
    )


def _set_objective_function(
    prob, assignment_var, warehouse_var, data: ProblemData, optimize: str
):
    """
    Sets the minimization objective for the optimization problem.

    Depending on 'optimize', the objective is either minimize total cost
    or total CO₂ emissions.

    - If optimize == "price": combines transport cost and warehouse rent
    - If optimize == "co2": combines transport emissions and warehouse emissions

    Args:
        prob: The PuLP LpProblem object.
        assignment_var: Dictionary of assignment decision variables (customer to warehouse).
        warehouse_var: Dictionary of warehouse selection decision variables.
        data: ProblemData instance containing input data and parameters.
        optimize: Objective type ("price" or "co2").
    """
    if optimize == "price":
        transport = _compute_transport_cost_term(assignment_var, data)
        warehouse = _compute_warehouse_cost_term(warehouse_var, data, "yearly_cost")
    else:
        transport = _compute_transport_co2_term(assignment_var, data)
        warehouse = _compute_warehouse_cost_term(
            warehouse_var, data, "yearly_co2_tons", multiplier=1000
        )
    prob += transport + warehouse


def _add_customer_assignment_constraints(prob, assignment_var, data: ProblemData):
    """
    Adds a constraint to ensure each customer is assigned to exactly one warehouse.
    """
    for c in data.df_customers.index:
        prob += (
            pulp.lpSum(assignment_var[(w, c)] for w in data.df_warehouses.index) == 1
        )


def _add_warehouse_selection_constraints(
    prob, assignment_var, warehouse_var, data: ProblemData
):
    """
    Adds a constraint to ensure customers are only assigned to warehouses that are selected (open).
    """
    for w in data.df_warehouses.index:
        for c in data.df_customers.index:
            prob += assignment_var[(w, c)] <= warehouse_var[w]


def _add_number_of_warehouses_constraints(
    prob, warehouse_var, data: ProblemData, number_of_warehouses
):
    """
    Adds a constraint to control how many warehouses can be selected.

    If a specific number is given, enforces that exact number.
    If 'any' is passed, allows between 1 and 10 warehouses.
    """
    warehouse_sum = pulp.lpSum(warehouse_var[w] for w in data.df_warehouses.index)
    if number_of_warehouses != "any":
        prob += warehouse_sum == int(number_of_warehouses)
    else:
        prob += warehouse_sum >= 1
        prob += warehouse_sum <= 10


def _add_country_constraints(prob, warehouse_var, data: ProblemData, country_list):
    """
    Adds constraints to enforce that at least one warehouse is selected in each specified country.
    """
    for country in country_list:
        wh_in_country = data.df_warehouses[
            data.df_warehouses["country"] == country
        ].index.tolist()
        prob += pulp.lpSum(warehouse_var[w] for w in wh_in_country) >= 1


def _add_excluded_country_constraints(
    prob, warehouse_var, data: ProblemData, no_country_list
):
    """
    Adds constraints to forbid selecting any warehouses in the specified countries.

    For each country in `no_country_list`, ensures no warehouse from that country is selected.
    """
    for country in no_country_list:
        wh_in_country = data.df_warehouses[
            data.df_warehouses["country"] == country
        ].index.tolist()
        if wh_in_country:  # skip if empty
            prob += pulp.lpSum(warehouse_var[w] for w in wh_in_country) == 0


def _add_constraints(
    prob,
    assignment_var,
    warehouse_var,
    data: ProblemData,
    number_of_warehouses,
    country_list=None,
    no_country_list=None,
):
    """
    Central helper that applies all constraints to the optimization problem.

    This includes:
    - Assigning each customer to one warehouse
    - Preventing assignments to unopened warehouses
    - Enforcing total warehouse count
    - Optionally enforcing warehouse presence in some countries
    - Optionally forbidding warehouse presence in some countries
    """
    _add_customer_assignment_constraints(prob, assignment_var, data)
    _add_warehouse_selection_constraints(prob, assignment_var, warehouse_var, data)
    _add_number_of_warehouses_constraints(
        prob, warehouse_var, data, number_of_warehouses
    )
    if country_list:
        _add_country_constraints(prob, warehouse_var, data, country_list)
    if no_country_list:
        _add_excluded_country_constraints(prob, warehouse_var, data, no_country_list)


def _interpret_solution(warehouse_var, assignment_var, data: ProblemData):
    """
    Interprets the optimized solution by extracting:
    - Which warehouses are selected
    - How customers are assigned to those warehouses
    - Total transport and fixed costs, as well as CO₂ emissions

    Returns structured data for formatting: selected warehouses, assignment details, and per-warehouse metrics.
    """
    selected_warehouses = [
        w for w in data.df_warehouses.index if pulp.value(warehouse_var[w]) == 1
    ]
    customers = data.df_customers.index.tolist()

    assignments = []
    scenario_costs = []
    scenario_co2s = []
    scenario_orders = []

    for w in selected_warehouses:
        yearly_cost = data.df_warehouses.at[w, "yearly_cost"]
        yearly_co2_tons = data.df_warehouses.at[w, "yearly_co2_tons"]
        total_transport_cost = 0
        total_transport_co2 = 0
        warehouse_orders = 0

        for c in customers:
            if pulp.value(assignment_var[(w, c)]) == 1:
                distance = data.distance_matrix.at[w, c]
                orders = data.df_customers.at[c, "yearly_orders"]

                total_transport_cost += distance * data.price_per_km * orders
                total_transport_co2 += distance * data.co2_per_km * orders
                warehouse_orders += orders

                assignments.append(
                    {
                        "warehouse": data.df_warehouses.at[w, "warehouse"],
                        "warehouse_lat": data.df_warehouses.at[w, "latitude"],
                        "warehouse_lon": data.df_warehouses.at[w, "longitude"],
                        "customer": data.df_customers.at[c, "company_name"],
                        "customer_lat": data.df_customers.at[c, "latitude"],
                        "customer_lon": data.df_customers.at[c, "longitude"],
                        "distance_km": distance,
                        "orders": orders,
                        "total_cost": int(distance * data.price_per_km * orders),
                        "total_co2_kg": int(distance * data.co2_per_km * orders),
                    }
                )

        scenario_costs.append(int(yearly_cost + total_transport_cost))
        scenario_co2s.append(int(yearly_co2_tons + total_transport_co2 / 1000))
        scenario_orders.append(warehouse_orders)

    return (
        selected_warehouses,
        assignments,
        scenario_costs,
        scenario_co2s,
        scenario_orders,
    )


def _format_results(
    data: ProblemData,
    selected_warehouses,
    assignments,
    scenario_costs,
    scenario_co2s,
    scenario_orders,
):
    """
    Takes structured solution data and converts it into two Pandas DataFrames:

    - df_selected: warehouse-level results with cost, CO₂, and total orders
    - df_assignments: detailed customer-to-warehouse assignment mapping

    These outputs are used for downstream analysis and visualization.
    """
    df_selected = data.df_warehouses.loc[selected_warehouses].copy()
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
    no_country_list=None,  ## Answer 3
    price_per_km=4,
    co2_per_km=2,
):
    """
    Builds and solves the warehouse optimization model using PuLP.

    This is the main function that ties everything together:
    - Prepares and encapsulates the input data
    - Defines decision variables for warehouse selection and customer assignments
    - Sets the objective function (optimize either total cost or total CO₂)
    - Adds all business constraints (assignment rules, warehouse limits, country requirements)
    - Solves the problem using the PuLP CBC solver
    - Extracts and formats the results into Pandas DataFrames

    Parameters:
        df_warehouses (pd.DataFrame): Info about candidate warehouses (location, cost, emissions, etc.)
        df_customers (pd.DataFrame): Info about customers (location, yearly orders, etc.)
        distance_matrix (pd.DataFrame): Distances between each warehouse and customer (in km)
        optimize (str): Whether to optimize for 'price' or 'co2' (default is 'price')
        number_of_warehouses (int or str): Either an integer (e.g. 3) or "any" for flexible count
        country_list (list or None): Optional list of countries to require at least one warehouse in each
        price_per_km (float): Transport cost per kilometer per order (default = 4)
        co2_per_km (float): Transport emissions per kilometer per order (default = 2)

    Returns:
        tuple:
            - df_selected (pd.DataFrame): Warehouses selected, with costs, CO₂, and orders handled
            - df_assignments (pd.DataFrame): Customer-to-warehouse assignments and their impact
    """
    data = ProblemData(
        df_warehouses.copy(),
        df_customers.copy(),
        distance_matrix.copy(),
        price_per_km,
        co2_per_km,
    )
    prob = _initialize_problem()
    warehouse_var, assignment_var = _define_variables(data)
    _set_objective_function(prob, assignment_var, warehouse_var, data, optimize)
    _add_constraints(
        prob,
        assignment_var,
        warehouse_var,
        data,
        number_of_warehouses,
        country_list,
        no_country_list,
    )
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    selected_warehouses, assignments, costs, co2s, orders = _interpret_solution(
        warehouse_var, assignment_var, data
    )
    return _format_results(data, selected_warehouses, assignments, costs, co2s, orders)
