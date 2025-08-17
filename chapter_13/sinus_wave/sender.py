import asyncio
import math
import random

import websockets

sampling_interval = 0.1  # Interval in seconds


async def send_sinus_wave(uri="ws://localhost:8765"):
    try:
        async with websockets.connect(uri) as websocket:
            t = 0  # Start time
            while True:
                y = math.sin(2 * math.pi * t)
                y = y * random.random()  # to add variability

                await websocket.send(str(y))
                print(f"Sending: {y}")
                await asyncio.sleep(sampling_interval)
                t += sampling_interval  # Increment time
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection was closed with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(send_sinus_wave())
