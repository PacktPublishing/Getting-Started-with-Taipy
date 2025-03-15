import math
import pickle
import socket
import time
from threading import Thread

import numpy as np
import pandas as pd
import requests
from taipy import Gui
from taipy.gui import Gui, State, get_state_id, invoke_callback, invoke_long_callback

HOST = "127.0.0.1"
PORT = 65432


def update_dataframe(new_data, df):
    """
    Update the DataFrame with new earthquake records from new_data.
    For each quake, check if its 'id' already exists in df.
    If not, process its fields and append it.

    new_data: List of earthquake features (each a dict from the USGS API)
    df: Existing DataFrame containing historical data.

    Returns an updated DataFrame.
    """
    new_rows = []  # List to hold records that need to be added
    existing_ids = set(df["id"])  # Set for faster membership testing

    for quake in new_data:
        quake_id = quake.get("id")
        # Check if the quake already exists in our DataFrame.
        if quake_id in existing_ids:
            continue  # Skip processing if record is already present

        properties = quake.get("properties", {})
        geometry = quake.get("geometry", {})

        # Process the time: convert epoch milliseconds to datetime.
        epoch_time = properties.get("time")
        time_dt = pd.to_datetime(epoch_time, unit="ms") if epoch_time else None

        mag = properties.get("mag")
        coords = geometry.get("coordinates", [])
        longitude = coords[0] if len(coords) >= 2 else None
        latitude = coords[1] if len(coords) >= 2 else None

        # Append the new row to our list.
        new_rows.append(
            {
                "id": quake_id,
                "time": time_dt,
                "mag": mag,
                "longitude": longitude,
                "latitude": latitude,
            }
        )

    if new_rows:
        # Create a DataFrame from the new rows and append to the historical DataFrame.
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new]).reset_index(drop=True)

    return df


# USGS API endpoint for the 10 most recent earthquakes
API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=10"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to server.")
    while True:
        try:
            response = requests.get(API_URL)
            data = response.json()
            earthquake_data = data.get("features", [])
            # Send the earthquake data as pickled bytes
            client_socket.sendall(pickle.dumps(earthquake_data))
            print("Sent earthquake data:")
            for quake in earthquake_data:
                mag = quake["properties"]["mag"]
                place = quake["properties"]["place"]
                print(f"  - Magnitude {mag} at {place}")
        except Exception as e:
            print("Error fetching or sending data:", e)
        time.sleep(10)  # Wait 10 seconds before next update


# Socket handler
def client_handler(gui: Gui, state_id_list: list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, _ = s.accept()
    while True:
        if data := conn.recv(1024 * 1024):
            pollutions = pickle.loads(data)
            print(f"Data received: {pollutions[:5]}")
            if hasattr(gui, "_server") and state_id_list:
                invoke_callback(
                    gui,
                    state_id_list[0],
                    update_pollutions,
                    [pollutions],
                )
        else:
            print("Connection closed")
            break


# Gui declaration
state_id_list = []

Gui.add_shared_variable("pollutions")


def on_init(state: State):
    state_id = get_state_id(state)
    if (state_id := get_state_id(state)) is not None and state_id != "":
        state_id_list.append(state_id)
    update_pollutions(state, pollutions)


def update_pollutions(state: State, val):
    state.pollutions = val
    state.data_province_displayed = pd.DataFrame(
        {
            "Latitude": lats,
            "Longitude": longs,
            "Pollution": state.pollutions,
        }
    )
    # Add an hour to the time
    state.periods = state.periods + 1
    state.max_pollutions = state.max_pollutions + [max(state.pollutions)]
    state.times = pd.date_range(
        "2020-11-04", periods=len(state.max_pollutions), freq="H"
    )
    state.line_data = pd.DataFrame(
        {
            "Time": state.times,
            "Max AQI": state.max_pollutions,
        }
    )


with tgb.Page() as earthquake_page:
    tgb.text("# Earthquake Data", mode="md")
    tgb.table("{df_earthquakes}", rebuild=True)


if __name__ == "__main__":

    df_earthquakes = pd.DataFrame(
        columns=["id", "time", "mag", "longitude", "latitude"]
    )

    gui = Gui(page=earthquake_page)

    t = Thread(
        target=client_handler,
        args=(
            gui,
            state_id_list,
        ),
    )
    t.start()
    gui.run()
