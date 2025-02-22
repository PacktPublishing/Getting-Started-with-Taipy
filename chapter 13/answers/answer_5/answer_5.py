import duckdb
import taipy.gui.builder as tgb
from taipy.gui import Gui


def query_dataframe(selected_dimension, dataset, min_tip, max_tip):
    conn = duckdb.connect()
    query = f"""
        SELECT
            {selected_dimension},
            tip_amount
        FROM
            '{dataset}'
        WHERE
            tip_amount BETWEEN {min_tip} AND {max_tip}
    """
    print(query)
    return conn.execute(query).fetchdf()


def change_dataframe(state):
    with state as s:
        s.min_tip, s.max_tip = s.tip_values[0], s.tip_values[1]
        s.df_stats = query_dataframe(
            s.selected_dimension, s.dataset, s.min_tip, s.max_tip
        )


with tgb.Page() as duck_db_page:
    tgb.text("# Using DuckDB", mode="md")
    with tgb.layout("1 1 1"):
        tgb.selector(
            value="{selected_dimension}",
            lov="{dimension_list}",
            label="Select dimension",
            dropdown=True,
        )
        tgb.slider(value="{tip_values}", min=0, max=430)

        tgb.button(label="Show Data!", on_action=change_dataframe)

    tgb.table("{df_stats}", rebuild=True)

if __name__ == "__main__":
    dimension_list = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "RatecodeID",
        "store_and_fwd_flag",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount",
        "congestion_surcharge",
        "Airport_fee",
    ]
    selected_dimension = "tpep_pickup_datetime"

    min_tip = 1
    max_tip = 10
    tip_values = [min_tip, max_tip]

    dataset = "./data/yellow_tripdata_2024-01.parquet"

    df_stats = query_dataframe(selected_dimension, dataset, min_tip, max_tip)

    gui = Gui(page=duck_db_page)
    gui.run(dark_mode=False, use_reloader=True)
