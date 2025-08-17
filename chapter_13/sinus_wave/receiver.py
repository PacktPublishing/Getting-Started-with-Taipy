import asyncio

import numpy as np
import websockets


# WebSocket Server
async def handler(websocket):
    print("Client connected!")

    # Define the maximum size of the buffer (2 full cycles, 200 samples for 1 Hz, 0.1 sec interval)
    buffer_size = 200
    sinus_buffer = np.zeros(buffer_size)  # Initialize an array to store sinus values

    # Keep track of the current index in the buffer
    current_index = 0

    try:
        async for message in websocket:
            new_value = float(message)

            # Store the new value in the buffer and update the index
            sinus_buffer[current_index] = new_value
            # Update index in a circular manner (when it reaches buffer_size, start overwriting)
            current_index = (current_index + 1) % buffer_size
            print(f"Updated Buffer: {sinus_buffer}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    finally:
        print("Connection closed!")


async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server is running on ws://localhost:8765")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
