import asyncio
import websockets
import json


async def get_data_from_dart():
    uri = "ws://127.0.0.1:8001/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to Dart server")

        # Send a request message
        await websocket.send("Requesting data")
        print("Message sent to server")

        # Wait for a response
        response = await websocket.recv()
        data = json.loads(response)
        print("Received data from server:", data)


# Run the asyncio event loop
asyncio.run(get_data_from_dart())
