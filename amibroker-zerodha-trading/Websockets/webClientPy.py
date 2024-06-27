import asyncio
import websockets
import sys
import json

async def send_signal():
    # Replace 'server_ip' with the actual IP address of the server machine
    uri = "wss://test-repo-ckt7.onrender.com"
    async with websockets.connect(uri) as websocket:
        signal_type = sys.argv[1]  # Signal type from command line argument
        symbol = sys.argv[2]       # Symbol from command line argument
        price = sys.argv[3]        # Price from command line argument

        message = json.dumps({
            "signal_type": signal_type,
            "symbol": symbol,
            "price": price
        })
        await websocket.send(message)
        print(f"Sent: {message}")

        # Optional: Receive response from server
        response = await websocket.recv()
        print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.run(send_signal())
