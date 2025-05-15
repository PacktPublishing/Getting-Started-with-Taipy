import asyncio

import requests
import websockets


def get_earthquakes(limit=10):
    earthquake_url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit={limit}"
    )
    response = requests.get(earthquake_url)

    return response


async def send_earthquake_data():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                print("getting data")
                earthquakes = get_earthquakes()

                await websocket.send(earthquakes)

                await asyncio.sleep(10)  # Wait for 10 seconds
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection was closed with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(send_earthquake_data())
