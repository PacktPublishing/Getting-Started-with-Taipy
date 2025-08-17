import asyncio

import numpy as np
import pandas as pd
import websockets

import taipy.gui.builder as tgb
from taipy import Gui
from taipy.gui import invoke_long_callback


# WebSocket Server
async def handler(websocket):
    global buffer_size
    global sinus_buffer
    print("Client connected!")
    current_index = 0
    try:
        async for message in websocket:
            new_value = float(message)
            sinus_buffer[current_index] = new_value
            current_index = (current_index + 1) % buffer_size
            print("update")

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


def on_init(state):
    invoke_long_callback(state, start_listening, [], update_sinus, [], 500)


with tgb.Page() as sinus_page:
    tgb.text("# Sinus wave", mode="md")

    tgb.chart("{sinus_series}", rebuild=True)


if __name__ == "__main__":
    buffer_size = 200
    sinus_buffer = np.zeros(buffer_size)

    sinus_series = pd.Series(sinus_buffer)
    gui = Gui(sinus_page)

    gui.run(dark_mode=False)  # use_reloader=True)
