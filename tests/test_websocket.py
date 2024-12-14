import pytest
import websockets
import asyncio

@pytest.mark.asyncio
async def test_websocket_order_updates(api_url):
    ws_uri = f'{api_url.replace("http", "ws")}/ws'

    websocket = None
    try:
        # Establish WebSocket connection
        websocket = await websockets.connect(ws_uri)
        await websocket.send("subscribe")
        
        # Receive response
        response = await websocket.recv()
        assert "connected" in response
        
    finally:
        if websocket and websocket.open:
            await websocket.close()

            