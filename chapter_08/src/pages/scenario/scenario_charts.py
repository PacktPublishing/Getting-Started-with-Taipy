import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_assignments(df_assignments):
    # Extract unique warehouses and customers
    df_warehouses_unique = df_assignments[
        ["warehouse", "warehouse_lat", "warehouse_lon"]
    ].drop_duplicates()
    df_warehouses_unique = df_warehouses_unique.rename(
        columns={"warehouse": "name", "warehouse_lat": "lat", "warehouse_lon": "lon"}
    )
    df_warehouses_unique["type"] = "Warehouse"

    df_customers_unique = df_assignments[
        ["customer", "customer_lat", "customer_lon"]
    ].drop_duplicates()
    df_customers_unique = df_customers_unique.rename(
        columns={"customer": "name", "customer_lat": "lat", "customer_lon": "lon"}
    )
    df_customers_unique["type"] = "Customer"

    data = pd.concat([df_warehouses_unique, df_customers_unique], ignore_index=True)

    # Prepare hover name and size
    data["hover_name"] = data.apply(
        lambda row: (
            f"Warehouse {row['name']}"
            if row["type"] == "Warehouse"
            else f"Customer: {row['name']}"
        ),
        axis=1,
    )
    data["size"] = data["type"].map({"Warehouse": 22, "Customer": 5})

    # Create the base figure with markers
    fig = px.scatter_map(
        data,
        lat="lat",
        lon="lon",
        color="type",
        color_discrete_map={"Customer": "blue", "Warehouse": "red"},
        size="size",
        hover_name="hover_name",
        hover_data={
            "lat": False,
            "lon": False,
            "type": False,
            "name": False,
            "size": False,
        },
        map_style="carto-positron",
        zoom=3,
        center={"lat": 50, "lon": 10},  # Center on Europe
        size_max=10,
    )

    # Prepare line coordinates for assignments
    lons = []
    lats = []
    for _, row in df_assignments.iterrows():
        lons.extend([row["warehouse_lon"], row["customer_lon"], None])
        lats.extend([row["warehouse_lat"], row["customer_lat"], None])

    # Add lines to the figure
    fig.add_trace(
        go.Scattermap(
            lon=lons,
            lat=lats,
            mode="lines",
            line=dict(width=1, color="#003399"),
            showlegend=False,
        )
    )

    # Customize layout similar to the example function
    fig.update_layout(
        title="📍 Customer-Warehouse Assignments",
        height=700,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
        ),
    )

    # Update hovertemplate to only show the hover_name
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><extra></extra>")

    return fig


def plot_customer_by_warehouse(df_assignments):
    fig = px.bar(
        df_assignments,
        x="warehouse",
        y="orders",
        color="customer",
        title="Orders per Warehouse by Customer",
        labels={"orders": "Number of Orders"},
        color_discrete_sequence=px.colors.qualitative.Set3,  # Use a qualitative colormap
    )
    return fig
