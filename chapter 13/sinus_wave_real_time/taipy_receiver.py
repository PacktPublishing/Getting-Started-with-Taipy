import asyncio

import numpy as np
import pandas as pd
import taipy.gui.builder as tgb
import websockets
from taipy import Gui
from taipy.gui import Gui, invoke_long_callback


async def handler(websocket):
    try:
        async for message in websocket:
            new_value = float(message)
            # Put the new value in the queue for the main thread
            await data_queue.put(new_value)

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    finally:
        print("Connection closed!")


async def listen():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server is running on ws://localhost:8765")
    await server.wait_closed()  # Keep the server running


def start_listening():
    asyncio.run(listen())


def update_sinus(state):
    print("updating")
    global sinus_buffer
    state.sinus_series = pd.Series(sinus_buffer)


def update_real_time(state):
    global sinus_buffer
    current_index = 0
    while True:
        try:
            new_value = data_queue.get_nowait()
            sinus_buffer[current_index] = new_value
            current_index = (current_index + 1) % buffer_size
            update_sinus(state)
            print("update")
        except asyncio.QueueEmpty:
            pass  # No new data, continue looping.
        except Exception as e:
            print(f"Error in main loop: {e}")
        import time

        time.sleep(0.001)


def update_sinus(state):
    print("updating")
    global sinus_buffer
    state.sinus_series = pd.Series(sinus_buffer)


def on_init(state):
    invoke_long_callback(state, start_listening, [])
    update_real_time(state)


with tgb.Page() as sinus_page:
    tgb.text("# Sinus wave", mode="md")

    tgb.chart("{sinus_series}", rebuild=True)


if __name__ == "__main__":
    buffer_size = 150
    sinus_buffer = np.zeros(buffer_size)
    data_queue = asyncio.Queue()

    sinus_series = pd.Series(sinus_buffer)
    gui = Gui(sinus_page)

    gui.run(dark_mode=False)  # use_reloader=True)
