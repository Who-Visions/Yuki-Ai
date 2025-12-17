import asyncio
import websockets
import json

async def test_websocket():
    # Uses a dummy ID
    uri = "ws://localhost:8080/ws/generation/test-gen-id-123"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                print(f"Received: {data}")
                if data['status'] in ['completed', 'failed']:
                     break
                await asyncio.sleep(1)
    except Exception as e:
        print(f"WS Error: {e}")

if __name__ == "__main__":
     asyncio.run(test_websocket())
