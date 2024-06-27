import asyncio
import websockets
import json

async def server(websocket, path):
    try:
        while True:
            data = await websocket.recv()  # Receive data from client
            print(f"Received data: {data}")
            
            parsed_data = json.loads(data)
            signal_type = parsed_data["signal_type"]
            symbol = parsed_data["symbol"]
            price = parsed_data["price"]

            print(f"Parsed data - Signal Type: {signal_type}, Symbol: {symbol}, Price: {price}")

            response = json.dumps({"status": "success", "message": f"Data processed: {parsed_data}"})
            await websocket.send(response)  # Send a response back to client
            print(f"Sent: {response}")
    except websockets.ConnectionClosed:
        print("Connection closed")

async def main():
    # Replace '0.0.0.0' with the server's IP address or 'localhost' if running on the same machine
    start_server = websockets.serve(server, "192.168.29.169", 8765)
    await start_server
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
