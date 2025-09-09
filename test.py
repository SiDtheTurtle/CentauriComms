import asyncio
import websockets

async def listen_to_websocket():
    """
    Connects to a WebSocket server and prints received messages.
    """
    # --- Configuration ---
    # Replace this with the address of your WebSocket server.
    # Using a public test server for this example.
    uri = "ws://192.168.107.184/websocket"

    print(f"Attempting to connect to {uri}...")

    try:
        # The 'async with' statement ensures the connection is closed properly.
        async with websockets.connect(uri) as websocket:
            print("WebSocket connection established successfully.")
            print("Listening for messages... (Press Ctrl+C to stop)")

            # The 'for' loop will run indefinitely, waiting for messages.
            async for message in websocket:
                # This will execute every time a message is received from the server.
                print(f"<- Received message: {message}")

    except websockets.exceptions.ConnectionClosedError:
        print("Connection with the server was closed.")
    except ConnectionRefusedError:
        print("Connection refused. Is the server running and accessible?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # asyncio.run() starts the asynchronous event loop.
    try:
        asyncio.run(listen_to_websocket())
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
