# import asyncio
# import socketio
# import json

# async def client():
#     sio = socketio.AsyncClient()

#     @sio.event
#     async def connect():
#         print('Connection established')

#     @sio.event
#     async def disconnect():
#         print('Disconnected from server')

#     @sio.event
#     async def response(data):
#         print(f"Received response: {data}")

#     await sio.connect('http://localhost:5000')
#     await sio.emit('signal', json.dumps({
#         "signal_type": "placeorder",
#         "variety": "regular",
#         "exchange": "NSE",
#         "tradingsymbol": "INFY",
#         "transaction_type": "BUY",
#         "quantity": 10,
#         "product": "CNC",
#         "order_type": "MARKET",
#         "price": None
#     }))
#     await sio.wait()

# if __name__ == "__main__":
#     asyncio.run(client())



import asyncio
import socketio
import json
import random

async def client():
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print('Connection established')

    @sio.event
    async def disconnect():
        print('Disconnected from server')

    @sio.event
    async def response(data):
        print(f"Received response: {data}")

    # await sio.connect('http://localhost:5000')
    # Serverlink
    await sio.connect('https://test-flask-ws-server-redeployed-main.onrender.com')

    for _ in range(40):  # Simulate sending 40 signals
        signal_type = random.choice(['placeorder', 'placegtt'])
        if signal_type == 'placeorder':
            data = json.dumps({
                "signal_type": "placeorder",
                "variety": "regular",
                "exchange": "NSE",
                "tradingsymbol": "INFY",
                "transaction_type": "BUY",
                "quantity": random.randint(1, 100),
                "product": "CNC",
                "order_type": "MARKET",
                "price": None
            })
        else:
            data = json.dumps({
                "signal_type": "placegtt",
                "trigger_type": "single",
                "tradingsymbol": "INFY",
                "exchange": "NSE",
                "trigger_values": [random.uniform(1500, 1600)],
                "last_price": random.uniform(1500, 1600),
                "orders": [
                    {
                        "transaction_type": "BUY",
                        "quantity": random.randint(1, 100),
                        "product": "CNC",
                        "order_type": "LIMIT",
                        "price": random.uniform(1500, 1600)
                    }
                ]
            })

        await sio.emit('signal', data)
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate varying intervals between signals

    await sio.wait()

if __name__ == "__main__":
    asyncio.run(client())
