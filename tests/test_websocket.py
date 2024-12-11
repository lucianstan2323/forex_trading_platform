import pytest
import websockets
import asyncio

@pytest.mark.asyncio
async def test_websocket_order_updates():
    async with websockets.connect("ws://localhost:8080/ws") as websocket:
        await websocket.send("subscribe")
        response = await websocket.recv()
        assert "connected" in response
