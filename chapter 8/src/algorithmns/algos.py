from math import atan2, cos, radians, sin, sqrt

import pandas as pd
import pulp


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance (in km) between two points on Earth.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * atan2(sqrt(a), sqrt(1 - a))  # Earth radius = 6371 km


def calculate_distance_matrix(df_warehouses, df_customers):
    """
    Returns a DataFrame where rows = warehouses, columns = customers,
    and values = distances in km.
    """
    df_warehouses["id"] = df_warehouses.index
    df_customers["id"] = df_customers.index  # 2 customers can have the same name
    distance_matrix = pd.DataFrame(
        index=df_warehouses["id"],
        columns=df_customers["id"],
        data=[
            [
                haversine(
                    wh_row["latitude"],
                    wh_row["longitude"],
                    cust_row["latitude"],
                    cust_row["longitude"],
                )
                for _, cust_row in df_customers.iterrows()
            ]
            for _, wh_row in df_warehouses.iterrows()
        ],
    )
    return distance_matrix


def create_pulp_model(
    df_warehouses,
    df_customers,
    distance_matrix,
    optimize: str,  # "price" or "co2"
    number_of_warehouses: int | str,  # e.g., 3 or "any"
    country_list: list = None,
    price_per_km: float = 4,
    co2_per_km: float = 2,
):
    """
    Creates and solves the optimization model.
    Returns:
        - Selected warehouses (DataFrame)
        - Assignments (DataFrame: warehouse, customer, distance, cost, co2)
    """
    # Taipy selector turns int into str:
    if number_of_warehouses != "any":
        number_of_warehouses = int(number_of_warehouses)

    df_warehouses["id"] = df_warehouses.index
    df_customers["id"] = df_customers.index  # 2 customers can have the same name

    # Initialize problem
    prob = pulp.LpProblem("Warehouse_Selection", pulp.LpMinimize)

    # Decision variables
    warehouses = df_warehouses["id"].tolist()
    customers = df_customers["id"].tolist()

    # x_w = 1 if warehouse w is selected
    warehouse_var = pulp.LpVariable.dicts("Warehouse", warehouses, cat="Binary")

    # y_wc = 1 if customer c is assigned to warehouse w
    assignment_var = pulp.LpVariable.dicts(
        "Assignment", [(w, c) for w in warehouses for c in customers], cat="Binary"
    )

    # Objective function
    if optimize == "price":
        # Total cost = warehouse rent + transportation cost
        transportation_cost = pulp.lpSum(
            assignment_var[(w, c)]
            * distance_matrix.at[w, c]
            * price_per_km
            * df_customers.at[c, "yearly_orders"]
            for w in warehouses
            for c in customers
        )
        total_cost = (
            pulp.lpSum(
                [
                    warehouse_var[w] * df_warehouses.at[w, "yearly_cost"]
                    for w in warehouses
                ]
            )
            + transportation_cost
        )
        prob += total_cost
    else:  # "co2"
        # Total CO2 = warehouse emissions + transportation emissions
        transportation_co2 = pulp.lpSum(
            assignment_var[(w, c)]
            * distance_matrix.at[w, c]
            * co2_per_km
            * df_customers.at[c, "yearly_orders"]
            for w in warehouses
            for c in customers
        )
        total_co2 = (
            pulp.lpSum(
                [
                    warehouse_var[w] * df_warehouses.at[w, "yearly_co2_tons"] * 1000
                    for w in warehouses
                ]  # Convert tons to kg
            )
            + transportation_co2
        )
        prob += total_co2

    # Constraints
    ## 1. Each customer assigned to exactly one warehouse
    for c in customers:
        prob += pulp.lpSum(assignment_var[(w, c)] for w in warehouses) == 1

    ## 2. Cannot assign to unopened warehouses
    for w in warehouses:
        for c in customers:
            prob += assignment_var[(w, c)] <= warehouse_var[w]

    ## 3. Number of warehouses
    if number_of_warehouses != "any":
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) == number_of_warehouses
    else:
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) >= 1
        prob += pulp.lpSum(warehouse_var[w] for w in warehouses) <= 10

    ## 4. Country constraints (if provided)
    if country_list:
        # Ensure at least one warehouse per country in country_list
        for country in country_list:
            wh_in_country = df_warehouses[df_warehouses["country"] == country][
                "id"
            ].tolist()
            prob += pulp.lpSum(warehouse_var[w] for w in wh_in_country) >= 1

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=True))  # Use CBC solver

    # Extract results
    selected_warehouses = [w for w in warehouses if pulp.value(warehouse_var[w]) == 1]

    assignments = []
    scenario_costs = []  # scenario per warehouse
    scenario_co2s = []  # scenario per warehouse
    scenario_orders = []
    for w in selected_warehouses:
        yearly_cost = df_warehouses.at[w, "yearly_cost"]
        yearly_co2_tons = df_warehouses.at[w, "yearly_co2_tons"]

        # Calculate total transportation cost, CO2 and total trips for this warehouse
        total_transport_cost = 0
        total_transport_co2 = 0
        warehouse_orders = 0
        for c in customers:
            if pulp.value(assignment_var[(w, c)]) == 1:
                # Get warehouse and customer coordinates
                wh_wh = df_warehouses.at[w, "warehouse"]
                wh_lat = df_warehouses.at[w, "latitude"]
                wh_lon = df_warehouses.at[w, "longitude"]
                cust_name = df_customers.at[c, "company_name"]
                cust_lat = df_customers.at[c, "latitude"]
                cust_lon = df_customers.at[c, "longitude"]

                # Calculate distance, cost, and CO2

                distance = distance_matrix.at[w, c]
                orders = df_customers.at[c, "yearly_orders"]

                total_transport_cost += distance * price_per_km * orders
                total_transport_co2 += distance * co2_per_km * orders
                warehouse_orders += orders

                assignments.append(
                    {
                        "warehouse": wh_wh,
                        "warehouse_lat": wh_lat,
                        "warehouse_lon": wh_lon,
                        "customer": cust_name,
                        "customer_lat": cust_lat,
                        "customer_lon": cust_lon,
                        "distance_km": distance,
                        "orders": orders,
                        "total_cost": int(
                            distance * price_per_km * orders
                        ),  # integer for better display
                        "total_co2_kg": int(
                            distance * co2_per_km * orders
                        ),  # integer for better display
                    }
                )
        # Add scenario cost and CO2 to the lists, as integers for better display
        scenario_costs.append(int(yearly_cost + total_transport_cost))
        scenario_co2s.append(
            int((yearly_co2_tons) + total_transport_co2 / 1000)
        )  # Retrieve CO2 emissions in metric tons
        scenario_orders.append(warehouse_orders)

    # Convert to DataFrames
    df_selected_warehouses = df_warehouses[
        df_warehouses["id"].isin(selected_warehouses)
    ].copy()
    df_assignments = pd.DataFrame(assignments)

    df_selected_warehouses["scenario_cost"] = scenario_costs
    df_selected_warehouses["scenario_co2_tons"] = scenario_co2s
    df_selected_warehouses["scenario_orders"] = scenario_orders

    return df_selected_warehouses, df_assignments


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
