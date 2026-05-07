import asyncio
import websockets

async def handler(ws):
    print("VTUBE CONNECTED")

    async for msg in ws:
        print("RECEIVED:", msg)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8001):
        print("✅ VTUBE SERVER RUNNING ws://127.0.0.1:8001")
        await asyncio.Future()

asyncio.run(main())