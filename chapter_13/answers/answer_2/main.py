import asyncio
import json
from datetime import datetime, timedelta, timezone

import chime  # OPTIONAL
import pandas as pd
import taipy.gui.builder as tgb
import websockets
from charts import create_earthquake_map
from taipy import Gui
from taipy.gui import Gui, invoke_long_callback, notify


async def handler(websocket):
    try:
        async for message in websocket:
            await data_queue.put(message)

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    finally:
        print("Connection closed!")


async def listen():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server is running on ws://localhost:8765")
    await server.wait_closed()


def start_listening():
    asyncio.run(listen())


def get_latest_minutes(minutes):
    now = datetime.now(timezone.utc)
    fiteen_minutes_ago = now - timedelta(minutes=minutes)
    return fiteen_minutes_ago


def get_now():
    now = datetime.now(timezone.utc)
    formatted_date_time = now.strftime("%d/%m/%Y 🕔 %H:%M:%S")
    return formatted_date_time


def process_quake(quake):
    """
    Process a single earthquake record and return a dictionary of its fields.

    Parameters:
        quake (dict): A dictionary containing earthquake data.
        current_time (datetime): The current time (timezone-aware) for calculating "last_hour".

    Returns:
        dict: A dictionary containing processed earthquake fields.
    """
    quake_id = quake.get("id")

    properties = quake.get("properties", {})
    geometry = quake.get("geometry", {})

    # Process the time: convert epoch milliseconds to datetime.
    epoch_time = properties.get("time")
    time_dt = pd.to_datetime(epoch_time, unit="ms", utc=True) if epoch_time else None

    mag = properties.get("mag")

    place = f"🌍 {properties.get('place')}"

    coords = geometry.get("coordinates", [])
    longitude = coords[0] if len(coords) >= 2 else None
    latitude = coords[1] if len(coords) >= 2 else None
    depth = coords[2] if len(coords) > 2 else None

    # Additional fields
    sig = properties.get("sig", 0)

    # Return the processed earthquake as a dictionary
    return {
        "id": quake_id,
        "time": time_dt,
        "mag": mag,
        "place": place,
        "longitude": longitude,
        "latitude": latitude,
        "depth": depth,
        "sig": sig,
    }


def update_dataframe(new_data, df, state=None):
    """
    Update the DataFrame with new earthquake records from new_data.
    For each quake, update the existing row if it exists, or append it as a new row.
    Recalculate the 'last_hour' column for all rows based on the current time.

    Parameters:
        new_data (list): List of earthquake features (each a dict from the USGS API).
        df (pd.DataFrame): Existing DataFrame containing historical data.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    # Create a set of existing IDs for faster lookup
    existing_ids = set(df["id"])

    # List to hold new rows
    new_rows = []

    # Process each earthquake in the new data
    for quake in new_data:
        mag = quake.get("properties", {}).get("mag")
        if mag and mag < 0:
            continue

        quake_id = quake.get("id")
        processed_quake = process_quake(quake)

        # If the earthquake already exists, update the row
        if quake_id in existing_ids:
            df.loc[df["id"] == quake_id, processed_quake.keys()] = (
                processed_quake.values()
            )
        else:
            # If the earthquake doesn't exist, add it to the new_rows list
            new_rows.append(processed_quake)

    # Append all new rows at once (if any)
    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new], ignore_index=True)

        if state:  # No state when called from the __main__
            print(f"""inserting...\n{new_rows}""")
            chime.info()  # Sound notification: we have new row
            notify(state, "w", "New earthquakes!")

    # Recalculate 'last_hour' for all rows based on the current time
    df["last_hour"] = df["time"].apply(
        lambda x: 1 if x >= get_latest_minutes(60) else 0
    )

    # Sort the DataFrame by time in descending order (latest earthquakes first)
    df = df.sort_values(by="time", ascending=False).reset_index(drop=True)

    return df


def update_earthquake(state, earthquakes):
    print("Updating Earthquake")

    state.df_earthquakes = update_dataframe(earthquakes, state.df_earthquakes, state)
    state.last_update = get_now()


def update_real_time(state):
    while True:
        try:
            earthquake_data = data_queue.get_nowait()
            earthquakes = json.loads(earthquake_data.decode("utf-8"))["features"]
            update_earthquake(state, earthquakes)
        except asyncio.QueueEmpty:
            pass  # No new data, continue looping.
        except Exception as e:
            print(f"Error in main loop: {e}")
        import time

        time.sleep(0.001)


def on_init(state):
    invoke_long_callback(state, start_listening, [])
    update_real_time(state)


with tgb.Page() as earthquake_page:
    with tgb.layout("1 1"):
        tgb.text("# **Earthquake** 🌍 Data", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("## Last Update: {last_update}", mode="md")

    tgb.chart(figure=lambda df_earthquakes: create_earthquake_map(df_earthquakes))

    tgb.table("{df_earthquakes}", date_format="yyyy-MM-dd 🕔 HH:mm:ss", rebuild=True)


if __name__ == "__main__":
    chime.theme("material")
    data_queue = asyncio.Queue()

    df_earthquakes = pd.DataFrame(
        columns=[
            "id",
            "time",
            "mag",
            "place",
            "longitude",
            "latitude",
            "depth",
            "last_hour",
            "sig",
        ]
    )
    last_update = get_now()

    gui = Gui(page=earthquake_page)

    gui.run(title="Earthquake 🌍 Data", dark_mode=False)  # , use_reloader=True)
