import pandas as pd
import pulp

from .problem_data import ProblemData


def _initialize_problem():
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
    return pulp.lpSum(
        assignment_var[(w, c)]
        * data.distance_matrix.at[w, c]
        * data.price_per_km
        * data.df_customers.at[c, "yearly_orders"]
        for w in data.df_warehouses.index
        for c in data.df_customers.index
    )


def _compute_transport_co2_term(assignment_var, data: ProblemData):
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
    return pulp.lpSum(
        warehouse_var[w] * data.df_warehouses.at[w, column] * multiplier
        for w in data.df_warehouses.index
    )


def _set_objective_function(
    prob, assignment_var, warehouse_var, data: ProblemData, optimize: str
):
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
    for c in data.df_customers.index:
        prob += (
            pulp.lpSum(assignment_var[(w, c)] for w in data.df_warehouses.index) == 1
        )


def _add_warehouse_selection_constraints(
    prob, assignment_var, warehouse_var, data: ProblemData
):
    for w in data.df_warehouses.index:
        for c in data.df_customers.index:
            prob += assignment_var[(w, c)] <= warehouse_var[w]


def _add_number_of_warehouses_constraints(
    prob, warehouse_var, data: ProblemData, number_of_warehouses
):
    if number_of_warehouses != "any":
        prob += pulp.lpSum(warehouse_var[w] for w in data.df_warehouses.index) == int(
            number_of_warehouses
        )
    else:
        prob += pulp.lpSum(warehouse_var[w] for w in data.df_warehouses.index) >= 1
        prob += pulp.lpSum(warehouse_var[w] for w in data.df_warehouses.index) <= 10


def _add_country_constraints(prob, warehouse_var, data: ProblemData, country_list):
    for country in country_list:
        wh_in_country = data.df_warehouses[
            data.df_warehouses["country"] == country
        ].index.tolist()
        prob += pulp.lpSum(warehouse_var[w] for w in wh_in_country) >= 1


def _add_constraints(
    prob,
    assignment_var,
    warehouse_var,
    data: ProblemData,
    number_of_warehouses,
    country_list,
):
    _add_customer_assignment_constraints(prob, assignment_var, data)
    _add_warehouse_selection_constraints(prob, assignment_var, warehouse_var, data)
    _add_number_of_warehouses_constraints(
        prob, warehouse_var, data, number_of_warehouses
    )
    if country_list:
        _add_country_constraints(prob, warehouse_var, data, country_list)


def _interpret_solution(warehouse_var, assignment_var, data: ProblemData):
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
    price_per_km=4,
    co2_per_km=2,
):
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
        prob, assignment_var, warehouse_var, data, number_of_warehouses, country_list
    )
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    selected_warehouses, assignments, costs, co2s, orders = _interpret_solution(
        warehouse_var, assignment_var, data
    )
    return _format_results(data, selected_warehouses, assignments, costs, co2s, orders)
