import time
from datetime import datetime, timedelta, timezone

import chime
import pandas as pd
import requests
from charts import create_earthquake_map

import taipy.gui.builder as tgb
from taipy import Gui
from taipy.gui import Gui, broadcast_callback, invoke_long_callback, notify


def get_now():
    now = datetime.now(timezone.utc)
    formatted_date_time = now.strftime("%d/%m/%Y 🕔 %H:%M:%S")
    return formatted_date_time


def get_earthquakes(limit=10):
    earthquake_url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit={limit}"
    )
    response = requests.get(earthquake_url)
    earthquakes = response.json()["features"]

    return earthquakes


def _get_latest_minutes(minutes):
    now = datetime.now(timezone.utc)
    return now - timedelta(minutes=minutes)


def notify_update(state):
    chime.info()  # Sound notification: we have new row
    notify(state, "w", "New earthquakes!")


def _get_last_hour(df):
    cutoff = _get_latest_minutes(60)
    df["last_hour"] = (df["time"] >= cutoff).astype(int)
    return df.sort_values(by="time", ascending=False, ignore_index=True)


def _process_quake(quake, quake_id):
    """
    Process a single earthquake record and return a dictionary of its fields.

    Parameters:
        quake (dict): A dictionary containing earthquake data.
        current_time (datetime): The current time (timezone-aware) for calculating "last_hour".

    Returns:
        dict: A dictionary containing processed earthquake fields.
    """
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

    sig = properties.get("sig", 0)
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


def _process_and_update_quake(quake, df, existing_ids):
    """
    Process a single quake and either update the DataFrame row
    or return it as a new row dict (if it's new).
    """
    mag = quake.get("properties", {}).get("mag", -1)
    if mag <= 0:
        return None

    quake_id = quake.get("id")
    processed_quake = _process_quake(quake, quake_id)

    if quake_id in existing_ids:
        df.loc[df["id"] == quake_id, processed_quake.keys()] = processed_quake.values()
        return None
    else:
        return processed_quake


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
    existing_ids = set(df["id"])
    new_rows = []
    for quake in new_data:
        result = _process_and_update_quake(quake, df, existing_ids)
        if result:
            new_rows.append(result)

    # Append all new rows at once (if any)
    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new], ignore_index=True)

        if state:  # No state when called from the __main__
            print(f"""inserting...\n{new_rows}""")
            broadcast_callback(state.get_gui(), notify_update)

    df = _get_last_hour(df)
    return df


def idle():
    """
    An infinite loop
    """

    while True:
        time.sleep(100)
        print("Listening...")


def on_init(state):
    """
    Start the update loop
    """
    gui = state.get_gui()
    # print(state.is_update_running) # You can uncomment this and open the app WITH DIFFERENT BROWSERS, you'll see how the is_update_running value becomes 1
    if state.is_update_running == 0:
        gui.broadcast_change("is_update_running", 1)
        invoke_long_callback(state, idle, [], update_earthquake, [], 60_000)


def update_earthquake(state):
    print("Updating Earthquake")
    earthquakes = get_earthquakes()

    updated_df_earthquakes = update_dataframe(earthquakes, state.df_earthquakes, state)

    gui.broadcast_change("df_earthquakes", updated_df_earthquakes)
    gui.broadcast_change("last_update", get_now())


with tgb.Page() as earthquake_page:
    with tgb.layout("1 1"):
        tgb.text("# **Earthquake** 🌍 Data", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("## Last Update: {last_update}", mode="md")

    tgb.chart(figure=lambda df_earthquakes: create_earthquake_map(df_earthquakes))

    tgb.table("{df_earthquakes}", date_format="yyyy-MM-dd 🕔 HH:mm:ss", rebuild=True)


if __name__ == "__main__":
    chime.theme("material")

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

    # Start with a bigger DataFrame
    df_earthquakes = update_dataframe(get_earthquakes(limit=50), df_earthquakes)

    # Variable to make sure we only launch one thread for the shared dataframe
    is_update_running = 0

    gui = Gui(page=earthquake_page)
    gui.add_shared_variable("df_earthquakes")
    gui.add_shared_variable("is_update_running")
    gui.add_shared_variable("last_update")
    gui.run(title="Earthquake 🌍 Data", dark_mode=False)  # , use_reloader=True)
