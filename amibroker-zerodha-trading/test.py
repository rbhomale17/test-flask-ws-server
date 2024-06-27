import asyncio
import websockets

async def hello():
    uri = "wss://test-repo-ckt7.onrender.com"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(hello())