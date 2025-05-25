import pandas as pd
import plotly.express as px


def plot_customers_warehouses(df_customers, df_warehouses):
    df_cust = df_customers.copy()
    df_wh = df_warehouses.copy()
    df_cust["type"] = "Customer"
    df_wh["type"] = "Warehouse"
    data = pd.concat([df_cust, df_wh])

    data["hover_amount"] = data.apply(
        lambda row: (
            f"Yearly Orders: {row['yearly_orders']}"
            if row["type"] == "Customer"
            else f"Yearly Rent: {row['yearly_cost']:,.0f} €"
        ),
        axis=1,
    )
    data["hover_name"] = data.apply(
        lambda row: (
            f"Company Name: {row['company_name']}"
            if row["type"] == "Customer"
            else f"Warehouse {row['warehouse']}"
        ),
        axis=1,
    )
    # Different marker size for Warehouses and customers
    data["size"] = data["type"].map({"Customer": 5, "Warehouse": 22})

    # Create the map
    fig = px.scatter_map(
        data,
        lat="latitude",
        lon="longitude",
        color="type",
        size="size",
        hover_name="hover_name",
        hover_data={
            "city": True,
            "hover_amount": True,
            "latitude": False,
            "longitude": False,
        },
        map_style="carto-positron",
        zoom=3,
        center={"lat": 50, "lon": 10},  # Center on Europe
        size_max=10,
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
    )
    # Customize legend (inside map, white background)
    fig.update_layout(
        title="📍 Customers & Potential Warehouses",
        height=700,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend=dict(
            x=0.02,
            y=0.98,  # Position: top-left inside the map
            bgcolor="rgba(255,255,255,0.8)",  # White semi-transparent background
            bordercolor="black",
            borderwidth=1,
        ),
    )

    return fig
